from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import settings

from api.models.databases import database
from .routers import users, assignments, comments


def configure() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup() -> None:
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await database.disconnect()

    app.include_router(comments.router)
    app.include_router(users.router)
    app.include_router(assignments.router)

    return app


api = configure()

