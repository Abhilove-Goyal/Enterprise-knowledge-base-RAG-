# from langchain_community.llms import Ollama 
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from config.settings import settings
llm = OllamaLLM(
    model=settings.GENERATION_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)
prompt = PromptTemplate.from_template("""
Generate 3 alternative search queries that help retrieve relevant documents.
Do NOT answer the question.
Orignal query:
{query}
Return each query on a new line.                                      
""")
def generate_multi_queries(query:str)->list[str]:
    response = llm.invoke(prompt.format(query=query))
    queries = [q.strip() for q in response.split("/n") if q.strip()]
    return queries 