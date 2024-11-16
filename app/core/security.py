import supabase

def verify_token(token: str):
    # Supabaseのクライアントインスタンスを作成
    supabase_client = supabase.create_client("<SUPABASE_URL>", "<SUPABASE_KEY>")
    user = supabase_client.auth.get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

