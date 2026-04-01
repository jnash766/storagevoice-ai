from typing import Any

from providers.base.provider import StorageProvider


class UnitTracProvider(StorageProvider):
    provider_key = "unittrac"
    display_name = "UnitTrac"

    async def validate_credentials(self, credentials: dict[str, Any]) -> tuple[bool, str]:
        # TODO: Replace with real UnitTrac OpenAPI credential verification call.
        if not credentials.get("base_url") or not credentials.get("api_key"):
            return False, "Missing required fields: base_url and api_key"
        return True, "Credentials look valid"

    async def get_available_units(self, filters: dict[str, Any]) -> dict[str, Any]:
        # TODO: Implement with UnitTrac OpenAPI.
        return {"provider": self.provider_key, "filters": filters, "units": []}

    async def verify_tenant(self, payload: dict[str, Any]) -> dict[str, Any]:
        # TODO: Implement with UnitTrac OpenAPI.
        return {"provider": self.provider_key, "verified": False, "details": payload}
