from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    LocalCreateUpdateMix)


class AudioMsgTranscriptionModel(Base, LocalCreateUpdateMix):
    __tablename__ = "audio_message_transcription"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    message_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("webhook_message.local_id"))

    attachment_id: Mapped[Optional[int]]
    url: Mapped[Optional[str]] = mapped_column(Text)
    text: Mapped[Optional[str]] = mapped_column(Text, default="")
    status: Mapped[Optional[int]]
