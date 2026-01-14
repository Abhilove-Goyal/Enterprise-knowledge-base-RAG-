import json
from collections import Counter

RESULTS_PATH = "evaluation/results.jsonl"

def normalize_human(label):
    mapping = {
        "correct": "grounded",
        "partially_correct": "partial",
        "incorrect": "hallucinated",
        "correct_refusal": "grounded"
    }
    return mapping.get(label)

def normalize_llm(verdict):
    mapping = {
        "grounded": "grounded",
        "partially_grounded": "partial",
        "hallucinated": "hallucinated"
    }
    return mapping.get(verdict)

records = []
with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

pairs = []
for r in records:
    human = normalize_human(r.get("human_label"))
    llm = normalize_llm(r["evaluation"]["faithfulness_verdict"])

    if human and llm:
        pairs.append((human, llm))

total = len(pairs)
agreement = sum(1 for h, l in pairs if h == l)

# Hallucination metrics
tp = sum(1 for h, l in pairs if l == "hallucinated" and h == "hallucinated")
fp = sum(1 for h, l in pairs if l == "hallucinated" and h != "hallucinated")
fn = sum(1 for h, l in pairs if l != "hallucinated" and h == "hallucinated")

precision = tp / (tp + fp) if (tp + fp) else 0
recall = tp / (tp + fn) if (tp + fn) else 0

metrics = {
    "total_evaluated": total,
    "exact_agreement_rate": round(agreement / total, 3),
    "hallucination_precision": round(precision, 3),
    "hallucination_recall": round(recall, 3)
}

print(json.dumps(metrics, indent=2))
