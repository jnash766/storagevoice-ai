import json
from dataclasses import dataclass

from sqlalchemy.orm import Session

from apps.api_service.src.models.audit_log import AuditLog
from apps.api_service.src.models.operator_contact import OperatorContact
from apps.api_service.src.models.provider_config import TenantProviderConfig
from apps.api_service.src.models.tenant import Tenant
from packages.common.security import SecretCipher
from providers.registry.factory import get_provider


@dataclass
class OnboardedTenant:
    tenant_id: str
    provider_key: str


class TenantService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._cipher = SecretCipher()

    async def onboard_tenant(
        self,
        business_name: str,
        provider_key: str,
        provider_base_url: str,
        provider_api_key: str,
        operator_phone_e164: str,
    ) -> OnboardedTenant:
        provider = get_provider(provider_key)
        is_valid, reason = await provider.validate_credentials(
            {"base_url": provider_base_url, "api_key": provider_api_key}
        )
        if not is_valid:
            raise ValueError(f"Provider credential validation failed: {reason}")

        tenant = Tenant(
            business_name=business_name,
        )
        self._db.add(tenant)
        self._db.flush()

        provider_config = TenantProviderConfig(
            tenant_id=tenant.id,
            provider_key=provider_key,
            encrypted_api_key=self._cipher.encrypt(provider_api_key),
            provider_base_url=provider_base_url,
        )
        self._db.add(provider_config)

        operator_contact = OperatorContact(tenant_id=tenant.id, phone_e164=operator_phone_e164)
        self._db.add(operator_contact)

        audit_log = AuditLog(
            tenant_id=tenant.id,
            event_type="tenant_onboarded",
            details=json.dumps(
                {
                    "provider_key": provider_key,
                    "provider_base_url": provider_base_url,
                    "operator_phone_e164": operator_phone_e164,
                }
            ),
        )
        self._db.add(audit_log)
        self._db.commit()
        self._db.refresh(tenant)
        return OnboardedTenant(tenant_id=str(tenant.id), provider_key=provider_key)
