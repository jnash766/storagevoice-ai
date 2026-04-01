from dataclasses import dataclass
from uuid import uuid4

from packages.common.security import SecretCipher
from providers.registry.factory import get_provider


@dataclass
class TenantRecord:
    tenant_id: str
    business_name: str
    provider_key: str
    encrypted_api_key: str
    provider_base_url: str
    operator_phone_e164: str


class TenantService:
    """
    In-memory service for scaffold phase.
    Replace with SQLAlchemy repository in next step.
    """

    def __init__(self) -> None:
        self._cipher = SecretCipher()
        self._tenants: dict[str, TenantRecord] = {}

    async def onboard_tenant(
        self,
        business_name: str,
        provider_key: str,
        provider_base_url: str,
        provider_api_key: str,
        operator_phone_e164: str,
    ) -> TenantRecord:
        provider = get_provider(provider_key)
        is_valid, reason = await provider.validate_credentials(
            {"base_url": provider_base_url, "api_key": provider_api_key}
        )
        if not is_valid:
            raise ValueError(f"Provider credential validation failed: {reason}")

        tenant_id = str(uuid4())
        record = TenantRecord(
            tenant_id=tenant_id,
            business_name=business_name,
            provider_key=provider_key,
            encrypted_api_key=self._cipher.encrypt(provider_api_key),
            provider_base_url=provider_base_url,
            operator_phone_e164=operator_phone_e164,
        )
        self._tenants[tenant_id] = record
        return record
