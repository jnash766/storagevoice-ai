from fastapi import FastAPI

from apps.api_service.src.routes.onboarding import router as onboarding_router

app = FastAPI(
    title="StorageVoice AI API",
    version="0.1.0",
    description="Multi-tenant backend for StorageVoice AI",
)

app.include_router(onboarding_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
