from fastapi import APIRouter
from .endpoints import auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

@api_router.get("/health-check")
async def health_check():
    return {"status": "ok"}