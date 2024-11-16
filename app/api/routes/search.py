from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.supabase import get_stocks
from app.services.cache import get_cache, set_cache
import logging

router = APIRouter()

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/api/search", response_model=List[dict])
async def search_stocks(
    query: Optional[str] = Query(None, min_length=1),
    limit: int = Query(10, gt=0),  # デフォルトで1ページあたり10件
    offset: int = Query(0, ge=0)   # デフォルトで最初のページ
):
    cache_key = f"search:{query}:{limit}:{offset}"
    logger.debug(f"Checking cache for key: {cache_key}")

    # キャッシュの確認
    cached_data = await get_cache(cache_key)
    if cached_data:
        logger.debug(f"Cache hit for key: {cache_key}")
        return cached_data

    try:
        # Supabaseからデータを取得
        results = await get_stocks(query=query, limit=limit, offset=offset)
        if not results:
            raise HTTPException(status_code=404, detail="No stocks found matching the query")

        # キャッシュに保存
        await set_cache(cache_key, results, ttl=300)  # キャッシュは5分間有効
        return results
    except HTTPException as http_exc:
        logger.error(f"HTTP error occurred: {http_exc.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error occurred")
