from config.supabase_client import supabase


def log_query(query_text: str, intent: str | None = None):
    if not supabase:
        return None

    res = supabase.table("rag_queries").insert({
        "query_text": query_text,
        "intent": intent
    }).execute()

    return res.data[0]["id"] if res.data else None


def log_answer(query_id: str, answer_text: str):
    if not supabase or not query_id:
        return None

    res = supabase.table("rag_answers").insert({
        "query_id": query_id,
        "answer_text": answer_text
    }).execute()

    return res.data[0]["id"] if res.data else None


def log_evaluation(answer_id: str, score: float | None, verdict: str | None):
    if not supabase or not answer_id:
        return None

    supabase.table("rag_evaluations").insert({
        "answer_id": answer_id,
        "faithfulness_score": score,
        "faithfulness_verdict": verdict
    }).execute()
