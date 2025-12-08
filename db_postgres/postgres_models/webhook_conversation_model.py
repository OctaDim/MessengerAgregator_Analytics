from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class WebhookConversationModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "webhook_conversation"

    id: Mapped[int] = mapped_column(primary_key=True)

    event: Mapped[str] = mapped_column(String(15))
    type: Mapped[str] = mapped_column(String(15))
    conversation_id: Mapped[int] = mapped_column()
    company_id: Mapped[int] = mapped_column()
    sender_name: Mapped[str] = mapped_column()
    sender_phone: Mapped[str] = mapped_column()
    sender_external_id: Mapped[str] = mapped_column()
    sender_external_public_id: Mapped[str] = mapped_column()
    provider: Mapped[str] = mapped_column(String(15))
    avatar_url: Mapped[str] = mapped_column()
    pact_created_at: Mapped[datetime] = mapped_column()
    pact_updated_at: Mapped[datetime] = mapped_column()
    last_message_id: Mapped[int] = mapped_column()
    operational_state: Mapped[str] = mapped_column(String(15))
    replied_state: Mapped[str] = mapped_column(String(15))
    group: Mapped[bool] = mapped_column(default=False)
