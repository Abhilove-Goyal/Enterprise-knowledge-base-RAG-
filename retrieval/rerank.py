# from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from config.settings import settings
from langchain_ollama import OllamaLLM
# Use a small, deterministic model for reranking
rerank_llm = OllamaLLM(
    model=settings.GENERATION_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)

rerank_prompt = PromptTemplate.from_template(
    """
You are ranking document chunks for relevance.

Query:
{query}

Chunk:
{chunk}

Score how relevant this chunk is for answering the query.
Give a score from 0 to 10.
ONLY return the number.
"""
)
def rerank(query, docs, rerank_mode="generic", top_n=None, min_score=None):
    """
    Rerank retrieved documents using an LLM.

    - Scores ALL docs
    - Filtering is OPTIONAL
    - No silent thresholds
    """

    top_n = top_n or settings.FINAL_TOP_K

    scored_docs = []

    for doc in docs:
        try:
            response = rerank_llm.invoke(
                rerank_prompt.format(
                    query=query,
                    chunk=doc.page_content[:1500]
                )
            )

            score = float(response.strip())
            scored_docs.append((score, doc))

        except Exception:
            # If LLM fails, still keep the doc with neutral score
            scored_docs.append((0.0, doc))

    # Sort by score
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    # OPTIONAL filtering (only if explicitly provided)
    if min_score is not None:
        scored_docs = [x for x in scored_docs if x[0] >= min_score]

    # Fallback: never return empty
    if not scored_docs:
        return docs[:top_n]

    return [doc for _, doc in scored_docs[:top_n]]
