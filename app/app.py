from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_db
from .routers import auth, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()  # ← crea las tablas al arrancar
    yield


app = FastAPI(title="Pokemon Team Builder", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(teams.router)
