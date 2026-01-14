import json
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin"])

METRICS_PATH = "evaluation/metrics_summary.json"

@router.get("/metrics")
def get_metrics():
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Metrics not generated yet"}
