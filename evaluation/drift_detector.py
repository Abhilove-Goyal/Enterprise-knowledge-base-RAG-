import json
from datetime import datetime, timedelta
from statistics import mean

RESULTS_PATH = "logs/results.jsonl"

BASELINE_DAYS = 7
CURRENT_DAYS = 1

DRIFT_THRESHOLDS = {
    "faithfulness_drop": 0.10,     # 10% drop
    "hallucination_increase": 0.15 # +15%
}

def parse_time(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def load_records():
    records = []
    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return records

def detect_drift():
    now = datetime.utcnow()
    baseline_cutoff = now - timedelta(days=BASELINE_DAYS)
    current_cutoff = now - timedelta(days=CURRENT_DAYS)

    baseline_scores = []
    baseline_hallu = []

    current_scores = []
    current_hallu = []

    for r in load_records():
        ts = parse_time(r["timestamp"])
        score = r.get("faithfulness_score")
        verdict = r.get("faithfulness_verdict")

        if score is None:
            continue

        if ts >= baseline_cutoff and ts < current_cutoff:
            baseline_scores.append(score)
            baseline_hallu.append(verdict == "hallucinated")

        if ts >= current_cutoff:
            current_scores.append(score)
            current_hallu.append(verdict == "hallucinated")

    if not baseline_scores or not current_scores:
        print("Not enough data for drift detection")
        return

    baseline_avg = mean(baseline_scores)
    current_avg = mean(current_scores)

    baseline_h_rate = sum(baseline_hallu) / len(baseline_hallu)
    current_h_rate = sum(current_hallu) / len(current_hallu)

    print("Baseline faithfulness:", round(baseline_avg, 3))
    print("Current faithfulness:", round(current_avg, 3))

    print("Baseline hallucination rate:", round(baseline_h_rate, 3))
    print("Current hallucination rate:", round(current_h_rate, 3))

    # --- Drift checks ---
    if baseline_avg - current_avg > DRIFT_THRESHOLDS["faithfulness_drop"]:
        print("🚨 DRIFT: Faithfulness dropped significantly")

    if current_h_rate - baseline_h_rate > DRIFT_THRESHOLDS["hallucination_increase"]:
        print("🚨 DRIFT: Hallucinations increased")

if __name__ == "__main__":
    detect_drift()
