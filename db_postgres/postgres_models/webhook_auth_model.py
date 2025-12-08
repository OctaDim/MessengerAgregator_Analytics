from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class WebhookAuthModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "webhook_auth"

    primary_id: Mapped[int] = mapped_column(primary_key=True)

    event: Mapped[str] = mapped_column(String(15))
    type: Mapped[str] = mapped_column(String(15))
    id: Mapped[int] = mapped_column()
    company_id: Mapped[int] = mapped_column()
    provider: Mapped[str] = mapped_column(String(15))
    state: Mapped[str] = mapped_column(String(15))
    phone_number: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sync_messages_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
