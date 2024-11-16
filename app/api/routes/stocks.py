from fastapi import APIRouter, HTTPException
from app.services.supabase import get_stock_details

router = APIRouter()

@router.get("/api/stocks/{stock_id}", response_model=dict)
async def get_stock_details_route(stock_id: int):
    try:
        stock = await get_stock_details(stock_id=stock_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

