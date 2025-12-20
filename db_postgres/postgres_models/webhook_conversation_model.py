from datetime import datetime
from typing import Optional

from sqlalchemy import String, BigInteger, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, LocalCreateUpdateMix)


class WebhookConversationModel(Base, ActiveMix, LocalCreateUpdateMix):
    __tablename__ = "webhook_conversation"

    local_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    event: Mapped[Optional[str]] = mapped_column(String(15))
    type: Mapped[Optional[str]] = mapped_column(String(15))
    id: Mapped[Optional[int]] = mapped_column(BigInteger)
    company_id: Mapped[Optional[int]]
    sender_name: Mapped[Optional[str]]
    sender_phone: Mapped[Optional[str]]
    sender_external_id: Mapped[Optional[str]]
    sender_external_public_id: Mapped[Optional[str]]
    provider: Mapped[Optional[str]] = mapped_column(String(30))
    avatar_url: Mapped[Optional[str]]  = mapped_column(String(255))
    last_message_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    operational_state: Mapped[Optional[str]] = mapped_column(String(15))
    replied_state: Mapped[Optional[str]] = mapped_column(String(15))
    group: Mapped[Optional[bool]]

    created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True))
    last_updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True))
