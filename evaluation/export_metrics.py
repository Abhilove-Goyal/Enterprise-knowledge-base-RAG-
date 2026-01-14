import json
import csv
from collections import defaultdict

INPUT_PATH = "evaluation/results.jsonl"
OUTPUT_PATH = "evaluation/metrics.csv"

rows = []

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        eval_data = r.get("evaluation", {})

        rows.append({
            "id": r["id"],
            "question_type": r["type"],
            "faithfulness_score": eval_data.get("faithfulness_score"),
            "verdict": eval_data.get("faithfulness_verdict"),
            "human_label": r.get("human_label"),
        })

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["id", "question_type", "faithfulness_score", "verdict", "human_label"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Metrics exported to {OUTPUT_PATH}")
