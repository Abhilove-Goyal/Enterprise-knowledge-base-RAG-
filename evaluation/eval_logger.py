import json
import os
from datetime import datetime, timezone

RESULTS_PATH = "logs/results.jsonl"

def log_evaluation(record: dict):
    os.makedirs("logs", exist_ok=True)
    record["evaluated_at"] = datetime.now(timezone.utc).isoformat()

    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
