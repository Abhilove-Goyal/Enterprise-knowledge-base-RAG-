from config.supabase_client import supabase

def log_query(query_text: str, intent: str | None = None):
    res = supabase.table("rag_queries").insert({
        "query_text": query_text,
        "intent": intent
    }).execute()

    return res.data[0]["id"]


def log_answer(query_id: str, answer_text: str):
    res = supabase.table("rag_answers").insert({
        "query_id": query_id,
        "answer_text": answer_text
    }).execute()

    return res.data[0]["id"]


def log_evaluation(answer_id: str, score: float | None, verdict: str | None):
    supabase.table("rag_evaluations").insert({
        "answer_id": answer_id,
        "faithfulness_score": score,
        "faithfulness_verdict": verdict
    }).execute()
