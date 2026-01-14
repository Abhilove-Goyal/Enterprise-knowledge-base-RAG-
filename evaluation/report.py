import json

BAD = 0
TOTAL = 0

with open("logs/interactions.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        eval_data = data.get("evaluation", {})
        score = eval_data.get("faithfulness_score")

        if score is not None:
            TOTAL += 1
            if score < 0.5:
                BAD += 1

print(f"Total evaluated answers: {TOTAL}")
print(f"Bad answers: {BAD}")
print(f"Failure rate: {BAD / TOTAL:.2%}" if TOTAL else "No evaluations yet")
