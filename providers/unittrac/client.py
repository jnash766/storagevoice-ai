"""HTTP client for UnitTrac OpenAPI v1 (Bearer API key).

Spec: https://www.unittrac.com/openapi/v1.json
"""

from __future__ import annotations

from typing import Any, Optional

import httpx


def normalize_base_url(base_url: str) -> str:
    base = base_url.strip().rstrip("/")
    if not base.startswith("http://") and not base.startswith("https://"):
        base = "https://" + base
    return base


class UnitTracClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout_s: float = 30.0,
        transport: Optional[Any] = None,
    ) -> None:
        self._base = normalize_base_url(base_url)
        self._api_key = api_key
        self._timeout = timeout_s
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._transport = transport

    def _url(self, path: str) -> str:
        base = self._base.rstrip("/")
        p = path if path.startswith("/") else f"/{path}"
        return base + p

    async def get_business_details(self) -> tuple[int, dict[str, Any] | None]:
        return await self._get_json("/api/v1/Businesses/details")

    async def list_facilities(self) -> tuple[int, list[dict[str, Any]] | None]:
        status, body = await self._get_json("/api/v1/Facilities")
        if status != 200 or body is None:
            return status, None
        if not isinstance(body, list):
            return status, None
        return status, body

    async def get_facility(self, facility_id: str) -> tuple[int, dict[str, Any] | None]:
        return await self._get_json(f"/api/v1/Facilities/{facility_id}")

    async def _get_json(self, path: str) -> tuple[int, Any]:
        url = self._url(path)
        client_kwargs: dict[str, Any] = {"timeout": self._timeout}
        if self._transport is not None:
            client_kwargs["transport"] = self._transport
        async with httpx.AsyncClient(**client_kwargs) as client:
            response = await client.get(url, headers=self._headers)
        if response.status_code == 204 or not response.content:
            return response.status_code, None
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, None
