import os
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String, Text, JSON, BigInteger, ForeignKey, TIMESTAMP)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class WebhookMessageModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "webhook_message"

    local_id: Mapped[int] = mapped_column(primary_key=True)
    conversation_local_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("webhook_conversation.local_id"))

    event: Mapped[Optional[str]] = mapped_column(String(15))
    type: Mapped[Optional[str]] = mapped_column(String(15))
    id: Mapped[Optional[int]] = mapped_column(BigInteger)
    external_id: Mapped[Optional[str]]
    company_id: Mapped[Optional[int]]
    conversation_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    contact_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    replied_to_id: Mapped[Optional[int]]
    income: Mapped[Optional[bool]]
    status: Mapped[Optional[str]] = mapped_column(String(15))
    message: Mapped[Optional[str]] = mapped_column(Text)
    reactions: Mapped[Optional[list]] = mapped_column(JSON)  # JSON
    details: Mapped[Optional[list]] = mapped_column(JSON)  # JSON
    attachments: Mapped[Optional[list]] = mapped_column(JSON)  # JSON

    created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True))
    external_created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True))

    file_name: Mapped[Optional[str]] = mapped_column(String(255))
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    push_to_talk: Mapped[Optional[bool]] = mapped_column(default=False)

    @hybrid_property
    def pty_file_name(self):
        valid_attachment_flag = all(
            [self.attachments, isinstance(self.attachments, list)])
        if valid_attachment_flag:
            property_value = self.attachments[0].get("file_name")
            return property_value
        else:
            return None

    @hybrid_property
    def pty_mime_type(self):
        valid_attachment_flag = all([self.attachments,
                                     isinstance(self.attachments, list)])
        if valid_attachment_flag:
            property_value = self.attachments[0].get("mime_type")
            return property_value
            # attachments = self.attachments[0]
            # attachment_file_name = attachments.get("file_name")
            # file_extension = os.path.splitext(attachment_file_name)[1]
            # attachment_mime_type = attachments.get("mime_type")
            # field_value = f"{file_extension} / {attachment_mime_type}"
            # return field_value
        else:
            return None

    # @file_name.expression
    # def file_name(cls):
    #     query_expression = case(
    #         (cls.attachments.isnot(None) &
    #          func.jsonb_array_length(cast(cls.attachments, type_=JSON)) > 0,
    #          cast(cls.attachments[0]["file_name"], String)),
    #         else_=cast(None, String))
    #     return query_expression

    # @file_mime_type.expression
    # def file_mime_type(cls):
    #     query_expression = case(
    #         (cls.attachments.isnot(None) &
    #          func.jsonb_array_length(cast(cls.attachments, type_=JSON)) > 0,
    #          cast(cls.attachments[0]["mime_type"], String)),
    #         else_=cast(None, String))
    #     return query_expression
