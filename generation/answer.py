from langchain_core.prompts import PromptTemplate
from config.settings import settings
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model=settings.GENERATION_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)

answer_prompt = PromptTemplate.from_template(
"""
Answer the question using the provided context.

Rules:
- Prioritize the provided context
- If the context partially answers the question, you may add minimal clarification
- Do NOT invent facts not implied by the context
- If the answer is unclear, say so explicitly

Context:
{context}

Question:
{question}

Answer:
"""
)

def generate_answer(query: str, docs: list) -> str:
    if not docs:
        return "I don't have enough information to answer this question."

    context = "\n\n".join(d.page_content for d in docs)

    response = llm.invoke(
        answer_prompt.format(
            context=context,
            question=query
        )
    )
    return response.strip()
