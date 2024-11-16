from postgrest import APIError
from supabase import create_client
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from fastapi import HTTPException

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_stocks(query: str = None, limit: int = 10, offset: int = 0):
    try:
        query_builder = supabase_client.table("stocks").select("*").limit(limit).offset(offset)

        if query:
            response = query_builder.ilike("name", f"*{query}*")

        response = query_builder.execute()
        
        return response.data
    except APIError as e:
        raise HTTPException(status_code=500, detail="Supabase API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_stock_details(stock_id: int):
    try:
        response = supabase_client.table("stocks").select("*").eq("id", stock_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Stock not found")
        return response.data[0]
    except APIError as e:
        raise HTTPException(status_code=500, detail="Supabase API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

