from fastapi import FastAPI

from apps.api_service.src.db.base import Base
from apps.api_service.src.db.session import engine
from apps.api_service.src import models  # noqa: F401
from apps.api_service.src.routes.onboarding import router as onboarding_router

app = FastAPI(
    title="StorageVoice AI API",
    version="0.1.0",
    description="Multi-tenant backend for StorageVoice AI",
)

app.include_router(onboarding_router)


@app.on_event("startup")
async def on_startup() -> None:
    # Keep startup simple for dev; Alembic migrations are the source of truth.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
