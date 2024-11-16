from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.supabase import get_stocks
import logging

router = APIRouter()

# ロギングの設定
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.supabase import get_stocks
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
    logger.debug(f"Received query: {query}, limit: {limit}, offset: {offset}")
    try:
        results = await get_stocks(query=query, limit=limit, offset=offset)
        if not results:
            raise HTTPException(status_code=404, detail="No stocks found matching the query")
        return results
    except HTTPException as http_exc:
        logger.error(f"HTTP error occurred: {http_exc.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected server error occurred")
