def clean_doc(doc):
    text = doc.page_content.strip()
    if len(text) < 100:
        return None
    if text.lower() in ["references","external links","category"]:
        return None
    doc.page_content = text
    return doc
def clean_documents(docs):
    return [d for d in (clean_doc(d) for d in docs) if d]
