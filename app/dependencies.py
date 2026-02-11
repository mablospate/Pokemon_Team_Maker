from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from .config import settings
from .database import get_session
from .models import User
from .routers.auth import TOKEN_LIFETIME

security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[Session, Depends(get_session)],
    response: Response,
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials, settings.secret_key, algorithms=["HS256"]
        )
        user = session.exec(select(User).where(User.id == payload["user_id"])).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        new_token = jwt.encode(
            {"user_id": user.id, "exp": datetime.now(timezone.utc) + TOKEN_LIFETIME},
            settings.secret_key,
            algorithm="HS256",
        )
        response.headers["X-Refreshed-Token"] = new_token
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
