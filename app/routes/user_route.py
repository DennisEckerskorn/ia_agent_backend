from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user
from app.core.jwt import create_access_token, get_current_user
from app.core.roles import require_admin
from app.db.crud.user_crud import (
    create_user, get_user_by_username,
    get_user_by_id, get_all_users, delete_user
)
from app.db.schemas.userschema import UserCreate, UserOut
from app.db.dependencies import get_db
from app.core.exceptions import UserAlreadyExists  # Agrega UserNotFound si lo creas

router = APIRouter(prefix="/users", tags=["Usuarios"])


# -------- LOGIN --------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autenticación de usuario, devuelve el token JWT.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "role": user.role}


# -------- USUARIO ACTUAL --------
@router.get("/me", response_model=UserOut)
def read_users_me(current_user=Depends(get_current_user)):
    """
    Devuelve los datos del usuario autenticado actual.
    """
    return current_user


# -------- REGISTRO DE USUARIOS NUEVOS --------
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    try:
        return create_user(db, user)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))


# -------- LISTAR TODOS LOS USUARIOS --------
@router.get("/listAll", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return get_all_users(db)


# -------- OBTENER USUARIO POR ID --------
@router.get("/getById/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario: {str(e)}")


# -------- ELIMINAR USUARIO --------
@router.delete("/delete/{user_id}", response_model=UserOut)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    try:
        user = delete_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {str(e)}")
