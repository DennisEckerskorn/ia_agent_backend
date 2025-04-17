from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import verify_password
from app.db.crud.user_crud import get_user_by_username


def authenticate_user(db: Session, username: str, password: str):
    """
    Autentica un usuario usando username y contraseña.
    """
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas (usuario)",
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas (contraseña)",
        )
    return user
