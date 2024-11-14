from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import api_router
from .core.config import settings
from .routers import auth, promotion, user

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


@app.get("/")
async def root():
    return {"message": "Welcome to Deals API"}
