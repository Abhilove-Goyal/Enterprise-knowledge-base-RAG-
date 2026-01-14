import json
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_PATH = "evaluation/results.jsonl"

rows = []

with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        rows.append({
            "id": r["id"],
            "type": r["type"],
            "faithfulness": r["evaluation"]["faithfulness_score"],
            "verdict": r["evaluation"]["faithfulness_verdict"],
            "human_label": r.get("human_label")
        })

df = pd.DataFrame(rows)
print(df.head())
plt.hist(df["faithfulness"].dropna(), bins=5)
plt.title("Faithfulness Score Distribution")
plt.xlabel("Score")
plt.ylabel("Count")
plt.show()
df.groupby("type")["faithfulness"].mean().plot(kind="bar")
plt.title("Average Faithfulness by Question Type")
plt.ylabel("Avg Faithfulness")
plt.show()
df["verdict"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Verdict Distribution")
plt.ylabel("")
plt.show()
eval_df = df[df["human_label"].notna()]

agreement = (eval_df["human_label"] == eval_df["verdict"]).mean()

print("Human–LLM Agreement:", round(agreement, 3))
