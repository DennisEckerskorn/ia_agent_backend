from fastapi import Depends, HTTPException, status
from app.core.jwt import get_current_user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a administradores"
        )
    return current_user


def require_user(current_user=Depends(get_current_user)):
    if current_user.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a usuarios autenticados"
        )
    return current_user
