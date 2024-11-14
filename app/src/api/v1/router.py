from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/health-check")
async def health_check():
    return {"status": "ok"}
