from typing import List
from sqlmodel import SQLModel, Field, Relationship


############################################################
#                        USER MODELS                       #
############################################################


class UserBase(SQLModel):
    username: str = Field(unique=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    username: str | None = None
    password: str | None = None


class UserPublic(UserBase):
    id: int


############################################################
#                     USER IN DATABASE                    #
############################################################


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    teams: List["Team"] = Relationship(back_populates="user")


############################################################
#                        TEAM MODELS                       #
############################################################


class TeamBase(SQLModel):
    name: str


class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = None


class TeamPublic(TeamBase):
    id: int
    user_id: int


class TeamPublicWithPokemon(TeamPublic):
    pokemon: List["PokemonPublic"] = []


############################################################
#                     TEAM IN DATABASE                    #
############################################################


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="teams")
    pokemon: list["Pokemon"] = Relationship(back_populates="team")


############################################################
#                      POKEMON MODELS                     #
############################################################


class PokemonBase(SQLModel):
    name: str


class PokemonCreate(PokemonBase):
    pass


class PokemonUpdate(SQLModel):
    name: str | None = None


class PokemonPublic(PokemonBase):
    id: int
    team_id: int


############################################################
#                    POKEMON IN DATABASE                   #
############################################################


class Pokemon(PokemonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tesm_id: int = Field(foreign_key="team.id")
    team: "Team" = Relationship(back_populates="pokemon")
