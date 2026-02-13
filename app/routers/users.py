from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..database import get_session
from ..dependencies import require_admin
from ..models import (
    Pokemon,
    Team,
    User,
    UserPublic,
    UserRoleUpdate,
)

router = APIRouter(prefix="/users", tags=["Admin"])


@router.patch("/{user_id}/role", response_model=UserPublic)
def change_user_role(
    user_id: int,
    data: UserRoleUpdate,
    admin: Annotated[User, Depends(require_admin)],
    session: Annotated[Session, Depends(get_session)],
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.role = data.role
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    admin: Annotated[User, Depends(require_admin)],
    session: Annotated[Session, Depends(get_session)],
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for team in user.teams:
        for pokemon in team.pokemon:
            session.delete(pokemon)
        session.delete(team)
    session.delete(user)
    session.commit()
    return {"msg": f"El usuario {user.username} ha sido eliminado"}
