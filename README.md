# Pokemon Team Builder

Aplicacion web para crear y gestionar equipos Pokemon. Proyecto personal de formacion centrado en el desarrollo de APIs REST con FastAPI.

**Demo:** https://pokemon-team-maker-ffbi.onrender.com/

## Funcionalidad

- **Registro e inicio de sesion** con autenticacion JWT y hashing de contrasenas con Argon2
- **Crear, renombrar y eliminar equipos** (cada usuario gestiona los suyos)
- **Anadir y quitar Pokemon** de un equipo (maximo 6 por equipo, niveles del 1 al 100)
- **Sprites automaticos** obtenidos de PokeAPI en el frontend
- **Documentacion interactiva** de la API en `/docs` (Swagger UI)

## Stack

| Capa          | Tecnologia                       |
| ------------- | -------------------------------- |
| Backend       | FastAPI + Uvicorn                |
| Base de datos | SQLite via SQLModel              |
| Auth          | JWT (PyJWT) + Argon2             |
| Frontend      | HTML + vanilla JS + Bootstrap 5 (generado con IA) |
| Deploy        | Docker + GitHub Actions + Render |

## API

La API es consumible de forma independiente al frontend. Todos los endpoints (salvo auth) requieren un token JWT en la cabecera `Authorization: Bearer <token>`.

| Metodo   | Ruta                               | Descripcion                          |
| -------- | ---------------------------------- | ------------------------------------ |
| `POST`   | `/auth/register`                   | Crear cuenta                         |
| `POST`   | `/auth/login`                      | Obtener token JWT                    |
| `GET`    | `/teams/`                          | Listar equipos del usuario           |
| `POST`   | `/teams/`                          | Crear equipo                         |
| `GET`    | `/teams/{id}`                      | Detalle de un equipo con sus Pokemon |
| `PATCH`  | `/teams/{id}`                      | Renombrar equipo                     |
| `DELETE` | `/teams/{id}`                      | Eliminar equipo                      |
| `POST`   | `/teams/{id}/pokemon`              | Anadir Pokemon al equipo             |
| `DELETE` | `/teams/{id}/pokemon/{pokemon_id}` | Quitar Pokemon del equipo            |

## Ejecutar en local

```bash
# Clonar y entrar
git clone https://github.com/<tu-usuario>/Pokemon_Team_Maker.git
cd Pokemon_Team_Maker

# Crear .env
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" > .env
echo "DATABASE_URL=sqlite:///pokemon.db" >> .env

# Instalar dependencias y arrancar
uv sync
uv run uvicorn app.app:app --reload
```

O con Docker:

```bash
docker build -t pokemon-team-builder .
docker run -p 8000:8000 pokemon-team-builder
```

La app estara disponible en `http://localhost:8000`.

## Nota sobre el frontend

El frontend (`front.html`) ha sido generado integramente con IA. El objetivo de este proyecto es la formacion en desarrollo de APIs REST con Python y FastAPI, no el desarrollo frontend. El frontend existe unicamente como interfaz visual para consumir y demostrar la API, pero todo el trabajo manual y el foco de aprendizaje esta en el backend: diseño de endpoints, modelos de datos, autenticacion, y despliegue.

## Sobre el proyecto

Este es un proyecto de formacion para aprender a construir APIs REST. La implementacion actual es deliberadamente simple: no tiene validacion exhaustiva de errores, los modelos son basicos y la base de datos es SQLite.

El plan es expandir la funcionalidad integrando la PokeAPI para que los equipos incluyan datos reales de cada Pokemon (stats, tipos, movimientos, habilidades) y se puedan exportar en formato importable a Pokemon Showdown.
