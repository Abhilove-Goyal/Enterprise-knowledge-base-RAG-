# config/supabase_client.py
import os
from typing import Optional

supabase = None  # default

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        # Log but NEVER crash the app
        print(f"[WARN] Supabase disabled: {e}")
