from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# -------------------- Config & DB --------------------
from config.settings import settings
from config.supabase_client import supabase
from db.logger import log_query, log_answer

# -------------------- Evaluation --------------------
from evaluation.async_evaluator import run_async_evaluation

# -------------------- RAG Pipeline --------------------
from embeddings.embedder import get_embeddings
from indexing.vectorstore import load_index
from retrieval.intent import classify_intent
from retrieval.rewrite import rewrite_query
from retrieval.multiquery import generate_multi_queries
from retrieval.hybrid import init_bm25, hybrid_retrieve_multiquery
from retrieval.rerank import rerank
from generation.answer import generate_answer

# -------------------- App Setup --------------------
app = FastAPI(title="Enterprise Knowledge RAG API")
templates = Jinja2Templates(directory="frontend/templates")

# -------------------- Load Vector Store (ONCE) --------------------
embeddings = get_embeddings()
vectorstore = load_index(embeddings, settings.INDEX_PATH)

documents = list(vectorstore.docstore._dict.values())
bm25 = init_bm25(documents)

# -------------------- Schemas --------------------
class Query(BaseModel):
    query: str

# -------------------- UI Routes --------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request}
    )

# -------------------- Metrics APIs (Supabase RPC) --------------------
@app.get("/admin/metrics/last-hour")
def metrics_last_hour():
    return (
        supabase
        .rpc("rag_metrics_window", {"hours_back": 1})
        .execute()
        .data
    )

@app.get("/admin/metrics/last-24h")
def metrics_last_24h():
    return (
        supabase
        .rpc("rag_metrics_window", {"hours_back": 24})
        .execute()
        .data
    )

# -------------------- Main RAG Endpoint --------------------
@app.post("/query")
def ask(q: Query, background_tasks: BackgroundTasks):
    user_query = q.query

    # ---- Intent (ONLY for routing, not blocking)
    intent = classify_intent(user_query)

    # ---- Retrieval
    rewritten_query = rewrite_query(user_query)
    queries = [rewritten_query] + generate_multi_queries(rewritten_query)

    candidate_docs = hybrid_retrieve_multiquery(
        vector_retriever=vectorstore.as_retriever(search_kwargs={"k": 30}),
        bm25_retriever=bm25,
        queries=queries,
        k=30
    )

    # ---- Rerank (NO THRESHOLDS)
    top_docs = rerank(
        query=user_query,
        docs=candidate_docs,
        rerank_mode=intent,
        top_n=5,          # fixed
        min_score=None    # <-- IMPORTANT
    )

    # ---- Generation (ALWAYS ANSWER)
    answer = generate_answer(user_query, top_docs)

    # ---- DB logging (core functionality)
    query_id = log_query(user_query, intent)
    answer_id = log_answer(query_id, answer)

    # ---- ASYNC evaluation (PASSIVE)
    if settings.ENABLE_EVALUATION:
        background_tasks.add_task(
            run_async_evaluation,
            query=user_query,
            answer=answer,
            docs=top_docs,
            answer_id=answer_id
        )

    return {
        "answer": answer,
        "sources": [
            d.metadata.get("source", "unknown")
            for d in top_docs
        ]
    }
