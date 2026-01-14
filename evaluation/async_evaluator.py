import threading
from evaluation.faithfulness import evaluate_faithfulness
from db.logger import log_evaluation

def run_async_evaluation(query, answer, docs, answer_id):
    try:
        score, verdict = evaluate_faithfulness(query, answer, docs)
        log_evaluation(answer_id, score, verdict)
    except Exception as e:
        print("Async evaluation failed:", e)
