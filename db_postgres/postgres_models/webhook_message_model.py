import json
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String, Text, DateTime, JSON, BigInteger, ForeignKey)
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class WebhookMessageModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "webhook_message"

    prim_id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("webhook_conversation.prim_id"))

    event: Mapped[Optional[str]] = mapped_column(String(15))
    type: Mapped[Optional[str]] = mapped_column(String(15))
    id: Mapped[Optional[int]] = mapped_column(BigInteger)
    external_id: Mapped[Optional[str]]
    company_id: Mapped[Optional[int]]
    contact_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    replied_to_id: Mapped[Optional[int]]
    income: Mapped[Optional[bool]]
    status: Mapped[Optional[str]] = mapped_column(String(15))
    message: Mapped[Optional[str]] = mapped_column(Text)
    reactions: Mapped[Optional[json]] = mapped_column(JSON)  # JSON
    details: Mapped[Optional[json]] = mapped_column(JSON)  # JSON
    attachments: Mapped[Optional[json]] = mapped_column(JSON)  # JSON

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True))
    external_created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True))
