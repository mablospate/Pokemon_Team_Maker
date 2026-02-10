from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models import User
from ..database import get_session
from ..dependencies import get_current_user
from ..models import (
    Pokemon,
    PokemonCreate,
    PokemonPublic,
    Team,
    TeamCreate,
    TeamPublic,
    TeamPublicWithPokemon,
    TeamUpdate,
    User,
)

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamPublic)
def create_team(
    data: TeamCreate,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    team = Team(name=data.name, user_id=user.id)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.get("/", response_model=list[TeamPublic])
def my_teams(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    return session.exec(select(Team).where(Team.user_id == user.id)).all()


@router.get("/{team_id}", response_model=TeamPublicWithPokemon)
def pokemon_in_team(
    team_id: int,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    team = session.exec(
        select(Team).where(team_id == Team.id, Team.user_id == user.id)
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return team


@router.patch("/{team_id}", response_model=TeamPublic)
def update_team_name(
    team_id: str,
    data: TeamUpdate,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    team = session.exec(
        select(Team).where(team_id == Team.id, Team.user_id == user.id)
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    team.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.delete("/{team_id}")
def remove_team(
    team_id: int,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    team = session.exec(
        select(Team).where(team_id == Team.id, Team.user_id == user.id)
    ).first()
    if not team:
        raise HTTPException(status_code=404)
    for pokemon in team.pokemon:
        session.delete(pokemon)
    session.delete(team)
    session.commit()
    return {"msg": f"El equipo {team.name} ha sido eliminado"}


@router.post("/{team_id}/pokemon", response_model=PokemonPublic)
def add_pokemon(
    team_id: int,
    data: PokemonCreate,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    team = session.exec(
        select(Team).where(team_id == Team.id, user.id == Team.user_id)
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if data.level <= 0 or data.level > 100:
        raise HTTPException(
            status_code=400, detail="El nivel debe tener un valor entre 0 y 100"
        )
    if len(team.pokemon) == 6:
        raise HTTPException(status_code=400, detail="El equipo ya tiene 6 pokemon")
    pokemon = Pokemon(
        name=data.name, species=data.species, level=data.level, team_id=team_id
    )
    session.add(pokemon)
    session.commit()
    session.refresh(pokemon)
    return pokemon


@router.delete("/{team_id}/pokemon/{pokemon_id}")
def delete_pokemon(
    team_id: str,
    pokemon_id: str,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    pokemon = session.exec(
        select(Pokemon).where(Pokemon.id == pokemon_id, Pokemon.team_id == team_id)
    ).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    team = session.exec(
        select(Team).where(Team.id == team_id, Team.user_id == user.id)
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    session.delete(pokemon)
    session.commit()
    return {
        "msg": f"El pokemon {pokemon.species} llamado {pokemon.name} ha sido eliminado"
    }
