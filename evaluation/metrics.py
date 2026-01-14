def recall_at_k(retrieved_docs, expected_text):
    for d in retrieved_docs:
        if expected_text.lower() in d.page_content.lower():
            return 1
    return 0

def mrr(retrieved_docs, gold_doc_ids):
    for i, d in enumerate(retrieved_docs):
        if d.metadata.get("id") in gold_doc_ids:
            return 1 / (i + 1)
    return 0.0
