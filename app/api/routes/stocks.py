from fastapi import APIRouter, HTTPException
from app.services.supabase import get_stock_details
from app.services.cache import get_cache, set_cache, delete_cache
import logging

router = APIRouter()

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/api/stocks/{stock_id}", response_model=dict)
async def get_stock_details_route(stock_id: int):
    cache_key = f"stock_details:{stock_id}"
    logger.debug(f"Checking cache for key: {cache_key}")

    # キャッシュの確認
    cached_stock = await get_cache(cache_key)
    if cached_stock:
        logger.debug(f"Cache hit for key: {cache_key}")
        return cached_stock

    try:
        # Supabaseからデータを取得
        stock = await get_stock_details(stock_id=stock_id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")

        # キャッシュに保存
        await set_cache(cache_key, stock, ttl=300)  # キャッシュは5分間有効
        return stock
    except HTTPException as http_exc:
        logger.error(f"HTTP error occurred: {http_exc.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error occurred")

