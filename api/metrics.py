from fastapi import APIRouter
from config.supabase_client import supabase

router = APIRouter()

@router.get("/metrics")
def get_metrics():
    response = supabase.rpc("get_rag_metrics").execute()

    if not response.data:
        return {
            "total_answers": 0,
            "avg_faithfulness": None,
            "hallucination_rate": 0,
            "grounded_rate": 0
        }

    return response.data[0]
