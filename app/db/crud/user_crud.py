from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.schemas.userschema import UserCreate
from app.core.security import hash_password
from app.core.exceptions import UserAlreadyExists


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise UserAlreadyExists(f"El usuario '{user.username}' ya está registrado.")

    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_pw,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
