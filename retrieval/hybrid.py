from langchain_community.retrievers import BM25Retriever
from typing import List
from langchain_core.documents import Document
from config.settings import settings


def init_bm25(documents: List[Document]) -> BM25Retriever:
    """
    Initialize BM25 retriever from documents.
    """
    bm25 = BM25Retriever.from_documents(documents)
    bm25.k = settings.BM25_TOP_K
    return bm25


def hybrid_retrieve_multiquery(
    vector_retriever,
    bm25_retriever,
    queries,
    k=15
):
    results = []

    for q in queries:
        # Vector search
        results.extend(vector_retriever.invoke(q))

        # BM25 search
        if bm25_retriever is not None:
            results.extend(bm25_retriever.invoke(q))

    # De-duplicate by content
    unique = {}
    for doc in results:
        unique[doc.page_content] = doc

    return list(unique.values())[:k]
