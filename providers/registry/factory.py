from providers.base.provider import StorageProvider
from providers.unittrac.provider import UnitTracProvider


_PROVIDERS: dict[str, type[StorageProvider]] = {
    UnitTracProvider.provider_key: UnitTracProvider,
}


def supported_providers() -> list[dict[str, str]]:
    return [
        {"key": key, "display_name": provider_class.display_name}
        for key, provider_class in _PROVIDERS.items()
    ]


def get_provider(provider_key: str) -> StorageProvider:
    provider_class = _PROVIDERS.get(provider_key)
    if provider_class is None:
        raise ValueError(f"Unsupported storage provider: {provider_key}")
    return provider_class()
