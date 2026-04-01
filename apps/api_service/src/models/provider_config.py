import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.api_service.src.db.base import Base


class TenantProviderConfig(Base):
    __tablename__ = "tenant_provider_configs"
    __table_args__ = (UniqueConstraint("tenant_id", "provider_key", name="uq_tenant_provider"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    provider_key: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_base_url: Mapped[str] = mapped_column(String(512), nullable=False)
    encrypted_api_key: Mapped[str] = mapped_column(String(4096), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    tenant = relationship("Tenant", back_populates="provider_configs")
