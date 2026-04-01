from pydantic import BaseModel, Field


class ProviderCredentials(BaseModel):
    base_url: str = Field(..., description="Provider API base URL")
    api_key: str = Field(..., description="Provider API key")


class TenantOnboardingRequest(BaseModel):
    business_name: str
    provider_key: str = Field(..., description="Selected storage software provider key")
    provider_credentials: ProviderCredentials
    operator_phone_e164: str


class TenantOnboardingResponse(BaseModel):
    tenant_id: str
    provider_key: str
    provider_status: str
