# from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import os 
from langchain_ollama import OllamaLLM
from config.settings import settings
llm = OllamaLLM(
    model=settings.GENERATION_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)
prompt = PromptTemplate.from_template("""
Rewrite the user's question to be clear, eexplicit, and retrieval-friendly.
    Do NOT answer the question.
    Orignal question:
    {query}
    Rewritten query:
""")
def rewrite_query(query:str)->str:
    rewritten = llm.invoke(prompt.format(query=query))
    return rewritten.strip()