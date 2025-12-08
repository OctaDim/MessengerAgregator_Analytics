from typing import Optional

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class MessageReactionsModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "message_reactions"

    primary_id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("webhook_message.prim_id"))

    reaction: Mapped[Optional[str]]
