from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import api_router
from .core.config import settings
from .routers import (
    auth,
    comment,
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


@app.get("/")
async def root():
    return {"message": "Welcome to Deals API"}
