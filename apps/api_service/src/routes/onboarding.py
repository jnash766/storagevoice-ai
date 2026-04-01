from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.api_service.src.db.session import get_db
from apps.api_service.src.schemas.onboarding import (
    TenantOnboardingRequest,
    TenantOnboardingResponse,
)
from apps.api_service.src.services.tenant_service import TenantService
from providers.registry.factory import supported_providers

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.get("/providers")
async def list_storage_software() -> list[dict[str, str]]:
    """
    Called by signup flow so operators can choose storage software.
    """
    return supported_providers()


@router.post("/tenant", response_model=TenantOnboardingResponse)
async def onboard_tenant(
    payload: TenantOnboardingRequest, db: Session = Depends(get_db)
) -> TenantOnboardingResponse:
    tenant_service = TenantService(db)
    try:
        tenant = await tenant_service.onboard_tenant(
            business_name=payload.business_name,
            provider_key=payload.provider_key,
            provider_base_url=payload.provider_credentials.base_url,
            provider_api_key=payload.provider_credentials.api_key,
            operator_phone_e164=payload.operator_phone_e164,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TenantOnboardingResponse(
        tenant_id=tenant.tenant_id,
        provider_key=tenant.provider_key,
        provider_status="connected",
    )
