from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import authenticate_user
from app.core.jwt import create_access_token, get_current_user
from app.db.crud.user_crud import create_user, get_user_by_username
from app.db.schemas.userschema import UserCreate, UserOut
from app.db.dependencies import get_db

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autenticación de usuario, Devuelve el token JWT
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user=Depends(get_current_user)):
    """
    Devuelve los datos del usuario autenticado actual.
    """
    return current_user