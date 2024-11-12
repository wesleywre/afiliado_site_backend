from app.database import get_db
from app.dependencies import get_current_user
from app.models.role import Role
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN


class RolePermissionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Obtenha a sessão do banco de dados
        db: Session = get_db()

        # Obtenha o usuário autenticado
        try:
            current_user = await get_current_user(
                db=db, token=request.headers.get("Authorization")
            )
        except HTTPException:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="User not authorized"
            )

        # Verifique se o endpoint exige alguma role específica
        required_role = request.scope.get("required_role")
        required_permission = request.scope.get("required_permission")

        # Verifique se o usuário possui a role necessária
        if required_role and not self._has_role(current_user, required_role, db):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Insufficient role"
            )

        # Verifique se o usuário possui a permissão necessária
        if required_permission and not self._has_permission(
            current_user, required_permission
        ):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Insufficient permission"
            )

        # Chame o próximo middleware ou endpoint
        response = await call_next(request)
        return response

    def _has_role(self, user, role_name: str, db: Session):
        # Carregar a role do banco de dados e verificar se o usuário possui a role
        role = db.query(Role).filter(Role.name == role_name).first()
        return role in user.role

    def _has_permission(self, user, permission_name: str):
        # Verificar se o usuário possui a perm. necessária em qualquer uma de suas roles
        for role in user.role:
            if any(
                permission.name == permission_name for permission in role.permissions
            ):
                return True
        return False
