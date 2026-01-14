import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("evaluation/metrics.csv")

# 1. Verdict distribution
df["verdict"].value_counts().plot(kind="bar", title="Verdict Distribution")
plt.show()

# 2. Faithfulness by question type
df.groupby("question_type")["faithfulness_score"].mean().plot(
    kind="bar", title="Avg Faithfulness by Question Type"
)
plt.show()
