import requests
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000/admin/metrics"

metrics = requests.get(API_URL).json()

labels = [
    "Avg Faithfulness",
    "Grounded Rate",
    "Hallucination Rate"
]

values = [
    metrics["avg_faithfulness"] or 0,
    metrics["grounded_rate"],
    metrics["hallucination_rate"]
]

plt.figure(figsize=(8, 5))
plt.bar(labels, values)
plt.ylim(0, 1)
plt.title("RAG System Health Dashboard")
plt.ylabel("Score / Rate")
plt.grid(axis="y")
plt.tight_layout()
plt.show()
