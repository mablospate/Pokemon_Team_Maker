from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_db
from .routers import auth, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()  # ← crea las tablas al arrancar
    yield


app = FastAPI(title="Pokemon Team Builder", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(teams.router)
