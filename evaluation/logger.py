from datetime import datetime, timezone
import json
import os
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_PATH = os.path.join(LOG_DIR, "interactions.jsonl")


def log_interaction(
    query: str,
    docs: list,
    answer: str,
    faithfulness_score: Optional[float] = None,
    faithfulness_verdict: Optional[str] = None
):
    os.makedirs(LOG_DIR, exist_ok=True)

    record = {
        "query": query,
        "answer": answer,
        "sources": [d.metadata.get("source", "unknown") for d in docs],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()   # 🔥 force write
