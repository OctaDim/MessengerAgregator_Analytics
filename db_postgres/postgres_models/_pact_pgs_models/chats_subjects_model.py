from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, LocalCreateUpdateMix)


class ChatsSubjectModel(Base, ActiveMix, LocalCreateUpdateMix):
    __tablename__ = "chats_subject_name"

    id: Mapped[int] = mapped_column(primary_key=True)

    chats_subject_name: Mapped[Optional[str]] = mapped_column(String(100))

    this_subject_conversations = relationship(
    # this_subject_conversations: Mapped[List["WebhookConversationModel"]] = relationship(
        argument="WebhookConversationModel",
        uselist=True,
        order_by="WebhookConversationModel.local_id.desc()",
        back_populates="this_conversation_subject",
    )
