from __future__ import annotations

from typing import Any

from providers.base.provider import StorageProvider
from providers.unittrac.client import UnitTracClient
from providers.unittrac.units import filter_available_units, find_unit_by_identifier


class UnitTracProvider(StorageProvider):
    provider_key = "unittrac"
    display_name = "UnitTrac"

    async def validate_credentials(self, credentials: dict[str, Any]) -> tuple[bool, str]:
        base_url = credentials.get("base_url")
        api_key = credentials.get("api_key")
        if not base_url or not api_key:
            return False, "Missing required fields: base_url and api_key"

        client = UnitTracClient(str(base_url), str(api_key))
        status, body = await client.get_business_details()
        if status == 401:
            return False, "Unauthorized: invalid UnitTrac API key"
        if status == 403:
            return False, "Forbidden: API key is not permitted for this resource"
        if status == 404:
            return False, "UnitTrac API endpoint not found (check base_url)"
        if status >= 500:
            return False, f"UnitTrac API error (HTTP {status})"
        if status != 200 or not isinstance(body, dict):
            return False, f"Unexpected UnitTrac response (HTTP {status})"

        return True, "Connected to UnitTrac"

    async def get_available_units(self, filters: dict[str, Any]) -> dict[str, Any]:
        base_url = filters.get("base_url")
        api_key = filters.get("api_key")
        facility_id = filters.get("facility_id")
        if not base_url or not api_key:
            return {
                "provider": self.provider_key,
                "error": "missing_base_url_or_api_key",
                "units": [],
            }
        if not facility_id:
            return {
                "provider": self.provider_key,
                "error": "facility_id_required",
                "units": [],
            }

        max_price = filters.get("max_price")
        max_price_f = float(max_price) if max_price is not None else None
        size_name_substring = filters.get("size_name_substring")
        size_filter = str(size_name_substring) if size_name_substring is not None else None

        client = UnitTracClient(str(base_url), str(api_key))
        status, facility = await client.get_facility(str(facility_id))
        if status == 401:
            return {"provider": self.provider_key, "error": "unauthorized", "units": []}
        if status == 404:
            return {"provider": self.provider_key, "error": "facility_not_found", "units": []}
        if status != 200 or not isinstance(facility, dict):
            return {
                "provider": self.provider_key,
                "error": f"unexpected_response_{status}",
                "units": [],
            }

        units = filter_available_units(
            facility,
            facility_id=str(facility_id),
            max_price=max_price_f,
            size_name_substring=size_filter,
        )
        return {"provider": self.provider_key, "facility_id": str(facility_id), "units": units}

    async def verify_tenant(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Best-effort verification using UnitTrac facility unit lists.

        The public UnitTrac v1 OpenAPI surface may not expose customer phone numbers.
        When phone cannot be verified via API, return unit_found + explicit next steps.
        """
        base_url = payload.get("base_url")
        api_key = payload.get("api_key")
        facility_id = payload.get("facility_id")
        unit_identifier = payload.get("unit_identifier") or payload.get("unit_number")
        phone_e164 = payload.get("phone_e164")

        if not base_url or not api_key:
            return {
                "provider": self.provider_key,
                "verified": False,
                "error": "missing_base_url_or_api_key",
            }
        if not facility_id or not unit_identifier:
            return {
                "provider": self.provider_key,
                "verified": False,
                "error": "facility_id_and_unit_identifier_required",
            }

        client = UnitTracClient(str(base_url), str(api_key))
        status, facility = await client.get_facility(str(facility_id))
        if status != 200 or not isinstance(facility, dict):
            return {
                "provider": self.provider_key,
                "verified": False,
                "error": f"facility_lookup_failed_{status}",
            }

        unit = find_unit_by_identifier(facility, str(unit_identifier))
        unit_found = unit is not None

        phone_verified = False
        if phone_e164 and unit_found:
            # Placeholder until UnitTrac exposes customer/lease phone fields on API keys we can access.
            phone_verified = False

        verified = bool(unit_found and phone_verified)
        return {
            "provider": self.provider_key,
            "verified": verified,
            "unit_found": unit_found,
            "phone_verified": phone_verified,
            "message": (
                "Unit identifier matched facility inventory."
                if unit_found
                else "Unit identifier not found in facility inventory."
            ),
        }
