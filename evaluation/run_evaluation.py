import json
from pathlib import Path
from datetime import datetime, timezone

# ---- Import your existing RAG pieces ----
from embeddings.embedder import get_embeddings
from indexing.vectorstore import load_index
from retrieval.intent import classify_intent
from retrieval.rewrite import rewrite_query
from retrieval.multiquery import generate_multi_queries
from retrieval.hybrid import init_bm25, hybrid_retrieve_multiquery
from retrieval.rerank import rerank
from generation.answer import generate_answer
from evaluation.faithfulness import evaluate_faithfulness
from config.settings import settings

# ---- Paths ----
QUESTIONS_PATH = Path("evaluation/questions.json")
OUTPUT_PATH = Path("evaluation/results.jsonl")

# ---- Load RAG once ----
print("Loading RAG components...")

embeddings = get_embeddings()
vectorstore = load_index(embeddings, settings.INDEX_PATH)

documents = list(vectorstore.docstore._dict.values())
bm25 = init_bm25(documents)

# ---- Load questions ----
with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

# ---- Run evaluation ----
OUTPUT_PATH.parent.mkdir(exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for q in questions:
        question = q["question"]
        print(f"\nEvaluating: {question}")

        intent = classify_intent(question)

        rewritten = rewrite_query(question)
        queries = [rewritten] + generate_multi_queries(rewritten)

        candidate_docs = hybrid_retrieve_multiquery(
            vector_retriever=vectorstore.as_retriever(
                search_kwargs={"k": settings.VECTOR_TOP_K}
            ),
            bm25_retriever=bm25,
            queries=queries,
            k=settings.BM25_TOP_K
        )

        top_docs = rerank(
            query=question,
            docs=candidate_docs,
            rerank_mode=intent,
            top_n=settings.FINAL_TOP_K,
            min_score=settings.RERANK_MIN_SCORE
        )

        answer = generate_answer(question, top_docs)

        # ---- Automated evaluation (optional) ----
        faithfulness_score, verdict = (None, None)
        if settings.ENABLE_EVALUATION:
            faithfulness_score, verdict = evaluate_faithfulness(
                question, answer, top_docs
            )

        record = {
            "id": q["id"],
            "question": question,
            "type": q["type"],
            "answer": answer,
            "sources": [
                d.metadata.get("source", "unknown") for d in top_docs
            ],
            "evaluation": {
                "faithfulness_score": faithfulness_score,
                "faithfulness_verdict": verdict
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "human_label": None,
            "notes": None
        }

        out.write(json.dumps(record, ensure_ascii=False) + "\n")

print("\nEvaluation complete. Results saved to evaluation/results.jsonl")
