from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class WebhookMessageModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "webhook_message"

    id: Mapped[int] = mapped_column(primary_key=True)

    event: Mapped[str] = mapped_column(String(15))
    type: Mapped[str] = mapped_column(String(15))
    message_id: Mapped[int] = mapped_column()
    external_id: Mapped[str] = mapped_column(String(255))
    company_id: Mapped[int] = mapped_column()
    conversation_id: Mapped[int] = mapped_column()
    contact_id: Mapped[int] = mapped_column()
    replied_to_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    pact_created_at: Mapped[datetime] = mapped_column()
    external_created_at: Mapped[datetime] = mapped_column()
    income: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(String(15))
    message: Mapped[str] = mapped_column(Text)
    reactions: Mapped[str] = mapped_column(Text, nullable=True)  # JSON как строка
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachments: Mapped[str] = mapped_column(Text, nullable=True)  # JSON как строка
