import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from .api.v1.router import api_router
from .core.config import settings
from .routers import (
    auth,
    comment,
    comment_like,
    coupon,
    moderation_comment,
    moderation_coupon,
    moderation_promotion,
    promotion,
    reaction,
    user,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar com as origens permitidas em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    redis_client = redis.from_url(
        "redis://new-kit-40601.upstash.io:6379",
        encoding="utf8",
        decode_responses=True,
        socket_timeout=1,
        socket_connect_timeout=1,
        retry_on_timeout=True,
        health_check_interval=30,
    )

    FastAPICache.init(RedisBackend(redis_client), prefix="promotions_coupons-cache:")


# Incluir rotas
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(promotion.router, prefix="/promotions", tags=["Promotions"])
app.include_router(user.router, tags=["Users"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(coupon.router, prefix="/coupons", tags=["Coupons"])
app.include_router(comment.router, prefix="/comments", tags=["Comments"])
app.include_router(reaction.router, prefix="/reactions", tags=["Reactions"])
app.include_router(
    moderation_promotion.router,
    prefix="/moderation/promotions",
    tags=["Moderation - Promotions"],
)
app.include_router(
    moderation_coupon.router,
    prefix="/moderation/coupons",
    tags=["Moderation - Coupons"],
)
app.include_router(
    moderation_comment.router,
    prefix="/moderation/comments",
    tags=["Moderation - Comments"],
)
app.include_router(
    comment_like.router,
    prefix="/comment-likes",
    tags=["Comment Likes"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Deals API"}
