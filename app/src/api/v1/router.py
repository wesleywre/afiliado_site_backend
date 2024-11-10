# app/src/api/v1/router.py
from fastapi import APIRouter

from .endpoints import auth, comments, coupons, likes, promotions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(promotions.router, prefix="/promotions", tags=["promotions"])
api_router.include_router(coupons.router, prefix="/coupons", tags=["coupons"])
api_router.include_router(likes.router, prefix="/likes", tags=["likes"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])


@api_router.get("/health-check")
async def health_check():
    return {"status": "ok"}
