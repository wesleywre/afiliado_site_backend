import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import role_permission, user, role, permission, coupon, promotion, comment, like, view
from app.api.endpoints import user as user_router
from app.api.endpoints import roles as role_router
from app.api.endpoints import permissions as permission_router
from app.api.endpoints import coupon as coupon_router
from app.api.endpoints import promotion as promotion_router
from app.api.endpoints import comment as comment_router
from app.api.endpoints import like as like_router
from app.api.endpoints import view as view_router
from app.api.deps import router as auth_router

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação da aplicação FastAPI
app = FastAPI()

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Adicione outros domínios permitidos aqui
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização do banco de dados
@app.on_event("startup")
def startup_event():
    logger.info("Starting up...")
    # Criação das tabelas no banco de dados
    user.Base.metadata.create_all(bind=engine)
    role.Base.metadata.create_all(bind=engine)
    permission.Base.metadata.create_all(bind=engine)
    coupon.Base.metadata.create_all(bind=engine)
    promotion.Base.metadata.create_all(bind=engine)
    comment.Base.metadata.create_all(bind=engine)
    like.Base.metadata.create_all(bind=engine)
    view.Base.metadata.create_all(bind=engine)
    role_permission.Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down...")

# Inclusão das rotas
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(role_router.router, prefix="/roles", tags=["roles"])
app.include_router(permission_router.router, prefix="/permissions", tags=["permissions"])
app.include_router(coupon_router.router, prefix="/coupons", tags=["coupons"])
app.include_router(promotion_router.router, prefix="/promotions", tags=["promotions"])
app.include_router(comment_router.router, prefix="/comments", tags=["comments"])
app.include_router(like_router.router, prefix="/likes", tags=["likes"])
app.include_router(view_router.router, prefix="/views", tags=["views"])

# Ponto de entrada principal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)