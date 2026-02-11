from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .database import create_db
from .routers import auth, teams

FRONT_HTML = Path(__file__).resolve().parent.parent / "front.html"


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


@app.get("/", include_in_schema=False)
async def serve_frontend():
    return FileResponse(FRONT_HTML)


# Esta linea está para poder repetir el despliegue de docker
