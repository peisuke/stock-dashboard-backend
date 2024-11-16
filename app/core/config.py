import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
UPSTASH_URL = os.getenv("UPSTASH_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_TOKEN")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

