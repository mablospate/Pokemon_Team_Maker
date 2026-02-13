import enum
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Role(str, enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


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
    role: Role


class UserRoleUpdate(SQLModel):
    role: Role


############################################################
#                     USER IN DATABASE                    #
############################################################


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    role: Role = Field(default=Role.USER)
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
    species: str
    level: int = Field(gt=0, le=100)


class PokemonCreate(PokemonBase):
    pass


class PokemonUpdate(SQLModel):
    name: str | None = None
    species: str | None = None
    level: int | None = Field(default=None, gt=0, le=100)


class PokemonPublic(PokemonBase):
    id: int
    team_id: int


############################################################
#                    POKEMON IN DATABASE                   #
############################################################


class Pokemon(PokemonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    team: "Team" = Relationship(back_populates="pokemon")
