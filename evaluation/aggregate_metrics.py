import json
from collections import defaultdict

RESULTS_PATH = "logs/results.jsonl"
OUTPUT_PATH = "evaluation/metrics_summary.json"

records = []
with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

total = len(records)

faith_scores = []
verdict_counts = defaultdict(int)
type_scores = defaultdict(list)
low_score_threshold = 0.6
low_score_count = 0

for r in records:
    eval_data = r.get("evaluation", {})
    score = eval_data.get("faithfulness_score")
    verdict = eval_data.get("faithfulness_verdict")
    q_type = r.get("type", "unknown")

    if score is not None:
        faith_scores.append(score)
        type_scores[q_type].append(score)

        if score < low_score_threshold:
            low_score_count += 1

    if verdict:
        verdict_counts[verdict] += 1

safe_avg = round(sum(faith_scores) / len(faith_scores), 3) if faith_scores else None

metrics = {
    "total_questions": total,
    "average_faithfulness": safe_avg,
    "verdict_distribution": dict(verdict_counts),
    "grounded_rate": round(verdict_counts.get("grounded", 0) / total, 3) if total else 0,
    "hallucination_rate": round(verdict_counts.get("hallucinated", 0) / total, 3) if total else 0,
    "low_score_rate": round(low_score_count / total, 3) if total else 0,
    "avg_faithfulness_by_type": {
        k: round(sum(v) / len(v), 3)
        for k, v in type_scores.items()
    }
}

print(json.dumps(metrics, indent=2))

# Save for dashboards / monitoring
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)
