# from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import os
# Use the shared settings instance
from config.settings import settings
# LLM for intent classification
from langchain_ollama import OllamaLLM
llm = OllamaLLM(
    model=settings.INTENT_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)

intent_prompt = PromptTemplate.from_template("""
Classify the intent of the question into ONE of the following categories:

- definition
- explanation
- comparison
- fact
- opinion

Question:
{query}

Return ONLY the intent name.
""")

def classify_intent(query: str) -> str:
    """
    Returns one of:
    definition | explanation | comparison | fact | opinion
    """
    intent = llm.invoke(
        intent_prompt.format(query=query)
    )
    return intent.strip().lower()
