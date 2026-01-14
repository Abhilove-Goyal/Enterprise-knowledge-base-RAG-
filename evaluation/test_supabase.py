from config.supabase_client import supabase

def test_insert():
    # 1️⃣ Insert query
    q_res = supabase.table("rag_queries").insert({
        "query_text": "Test query from Python"
    }).execute()

    print("Query insert:", q_res)

    query_id = q_res.data[0]["id"]

    # 2️⃣ Insert answer (FK-safe)
    a_res = supabase.table("rag_answers").insert({
        "query_id": query_id,
        "answer_text": "This is a test answer"
    }).execute()

    print("Answer insert:", a_res)

if __name__ == "__main__":
    test_insert()
