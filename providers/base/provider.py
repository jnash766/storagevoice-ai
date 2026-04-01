from abc import ABC, abstractmethod
from typing import Any


class StorageProvider(ABC):
    """Provider-agnostic interface for storage management system integrations."""

    provider_key: str
    display_name: str

    @abstractmethod
    async def validate_credentials(self, credentials: dict[str, Any]) -> tuple[bool, str]:
        pass

    @abstractmethod
    async def get_available_units(self, filters: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    async def verify_tenant(self, payload: dict[str, Any]) -> dict[str, Any]:
        pass
