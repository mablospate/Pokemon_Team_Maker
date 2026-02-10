from typing import Annotated

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..config import settings
from ..database import get_session
from ..models import User, UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["Auth"])
ph = PasswordHasher()


@router.post("/register", response_model=UserPublic)
def register(data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    existing = session.exec(select(User).where(User.username == data.username)).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Este nombre de usuario ya existe en la base de datos",
        )
    user = User(username=data.username, hashed_password=ph.hash(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login")
def login(data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    user = session.exec(select(User).where(User.username == data.username)).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Este nombre de usuario no existe en la base de datos",
        )
    try:
        ph.verify(user.hashed_password, data.password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=401, detail="Nombre de usuario o contraseña incorrectos"
        )
    token = jwt.encode({"user_id": user.id}, settings.secret_key, algorithm="HS256")
    return {"access_token": token}
