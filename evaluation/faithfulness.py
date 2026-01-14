import json
import re
from typing import Tuple, Optional
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from config.settings import settings

judge_llm = OllamaLLM(
    model=settings.RERANK_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)

faithfulness_prompt = PromptTemplate.from_template("""
You are evaluating whether the answer is fully supported by the context.

Context:
{context}

Question:
{query}

Answer:
{answer}

Respond ONLY in valid JSON like this:
{{
  "score": number between 0 and 1,
  "verdict": "grounded" | "partially_grounded" | "hallucinated"
}}
""")

def extract_json(text: str) -> Optional[dict]:
    """
    Extract first JSON object from LLM output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None

def evaluate_faithfulness(query: str, answer: str, docs: list) -> Tuple[Optional[float], str]:
    try:
        context = "\n\n".join(d.page_content for d in docs)

        response = judge_llm.invoke(
            faithfulness_prompt.format(
                query=query,
                answer=answer,
                context=context
            )
        )

        data = extract_json(response)

        if not data:
            return None, "evaluation_failed"

        score = float(data.get("score"))
        verdict = data.get("verdict")

        if verdict not in {"grounded", "partially_grounded", "hallucinated"}:
            return None, "evaluation_failed"

        return score, verdict

    except Exception:
        return None, "evaluation_failed"
