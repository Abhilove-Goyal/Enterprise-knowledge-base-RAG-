from datetime import datetime
from config.supabase_client import supabase
from evaluation.alert_thresholds import THRESHOLDS

ALERT_LOG = "logs/alerts.log"

def check_alerts(hours_back=24):
    res = (
        supabase
        .rpc("rag_metrics_window", {"hours_back": hours_back})
        .execute()
    )

    if not res.data:
        print("⚠️ No metrics available")
        return

    metrics = res.data[0]
    alerts = []

    avg_faithfulness = metrics.get("avg_faithfulness")
    hallucination_rate = metrics.get("hallucination_rate")

    if avg_faithfulness is not None and \
       avg_faithfulness < THRESHOLDS["average_faithfulness"]:
        alerts.append("🚨 Avg faithfulness below SLO")

    if hallucination_rate is not None and \
       hallucination_rate > THRESHOLDS["hallucination_rate"]:
        alerts.append("🚨 Hallucination rate too high")

    if alerts:
        with open(ALERT_LOG, "a", encoding="utf-8") as f:
            for a in alerts:
                f.write(f"{datetime.utcnow().isoformat()} | {a}\n")

        print("ALERTS:")
        for a in alerts:
            print(a)
    else:
        print("System healthy ✔")

if __name__ == "__main__":
    check_alerts()
