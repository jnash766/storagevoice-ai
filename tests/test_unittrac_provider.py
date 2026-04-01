import asyncio

import httpx

from providers.unittrac.provider import UnitTracProvider


def test_get_business_details_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("Authorization") == "Bearer good"
        if "/api/v1/Businesses/details" in str(request.url):
            return httpx.Response(
                200,
                json={
                    "id": "business_1",
                    "name": "Acme",
                    "phone": "(111) 222-3333",
                    "email": "a@b.com",
                },
            )
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    from providers.unittrac.client import UnitTracClient

    async def run() -> None:
        ut = UnitTracClient("https://www.unittrac.com", "good", transport=transport)
        status, body = await ut.get_business_details()
        assert status == 200
        assert isinstance(body, dict)
        assert body.get("id") == "business_1"

    asyncio.run(run())


def test_get_business_details_unauthorized() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401)

    transport = httpx.MockTransport(handler)
    from providers.unittrac.client import UnitTracClient

    async def run() -> None:
        ut = UnitTracClient("https://www.unittrac.com", "bad", transport=transport)
        status, _ = await ut.get_business_details()
        assert status == 401

    asyncio.run(run())


def test_provider_validate_credentials_uses_live_client() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if "/api/v1/Businesses/details" in str(request.url):
            return httpx.Response(200, json={"id": "b", "name": "n", "phone": "p", "email": "e"})
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    provider = UnitTracProvider()

    from providers.unittrac import provider as mod

    original = mod.UnitTracClient

    def factory(base_url: str, api_key: str) -> object:
        return original(base_url, api_key, transport=transport)

    mod.UnitTracClient = factory  # type: ignore[misc]
    try:

        async def run() -> None:
            ok, msg = await provider.validate_credentials(
                {"base_url": "https://www.unittrac.com", "api_key": "k"}
            )
            assert ok is True
            assert "UnitTrac" in msg

        asyncio.run(run())
    finally:
        mod.UnitTracClient = original
