from typing import Optional

from sqlalchemy import ForeignKey, BigInteger, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, LocalCreateUpdateMix)


class MessageAttachmentsModel(Base, ActiveMix, LocalCreateUpdateMix):
    __tablename__ = "message_attachments"

    local_id: Mapped[int] = mapped_column(primary_key=True)
    message_local_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("webhook_message.local_id"))

    event: Mapped[Optional[str]] = mapped_column(String(15))
    type: Mapped[Optional[str]] = mapped_column(String(15))

    id: Mapped[Optional[int]] = mapped_column(BigInteger)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    file_name: Mapped[Optional[str]]
    mime_type: Mapped[Optional[str]]
    size: Mapped[Optional[int]]
    attachment_url: Mapped[Optional[str]]
    preview_url: Mapped[Optional[str]]
    aspect_ratio: Mapped[Optional[float]]
    data: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    push_to_talk: Mapped[Optional[bool]] = mapped_column(default=False)
