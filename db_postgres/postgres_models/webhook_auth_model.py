from datetime import datetime
from typing import Optional

from sqlalchemy import String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class WebhookAuthModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "webhook_auth"

    local_id: Mapped[int] = mapped_column(primary_key=True)

    event: Mapped[Optional[str]] = mapped_column(String(15))
    type: Mapped[Optional[str]] = mapped_column(String(15))
    id: Mapped[Optional[int]]
    company_id: Mapped[Optional[int]]
    provider: Mapped[Optional[str]] = mapped_column(String(30))
    state: Mapped[Optional[str]] = mapped_column(String(15))
    phone_number: Mapped[Optional[str]]

    created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True))
    sync_messages_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True))
