def compute_answer_confidence(
    query: str,
    answer: str,
    docs: list,
    intent: str
) -> dict:
    """
    Returns confidence decision and reasons
    """

    reasons = []

    # --- Rule 1: Too few docs ---
    if len(docs) < 2:
        reasons.append("insufficient_retrieval")

    # --- Rule 2: Weak rerank score ---
    scores = [
        d.metadata.get("score", 0)
        for d in docs
    ]
    max_score = max(scores) if scores else 0
    if max_score < 0.3:
        reasons.append("low_relevance")

    # --- Rule 3: Very short answer ---
    if len(answer.split()) < 40:
        reasons.append("answer_too_short")

    # --- Rule 4: Ambiguous intent ---
    if intent == "ambiguous":
        reasons.append("ambiguous_query")

    confident = len(reasons) == 0

    return {
        "confident": confident,
        "reasons": reasons,
        "max_score": round(max_score, 3),
        "doc_count": len(docs)
    }
def fallback_response(confidence):
    if "ambiguous_query" in confidence["reasons"]:
        return "Your question seems a bit broad. Could you clarify what specifically you want to know?"

    if "insufficient_retrieval" in confidence["reasons"]:
        return "I couldn’t find enough reliable information to answer this confidently."

    return "I’m not confident enough in this answer. Please try rephrasing the question."
