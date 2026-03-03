from datetime import datetime
from typing import Literal, Optional, Any

from pydantic import field_validator

from fast_api.app_global_api_webhooks.router_schemes.scheme_new_message import (
    NewMessageData)


class MessageEditedData(NewMessageData):
    event_type: Literal["MessageEdited"]  # discriminator="MessageEdited"

    ev_edit_date: Optional[datetime]

    reactions_total_custom: Optional[dict]
    reactions_total_count_custom: Optional[int]
    reactions_emoticon_custom: Optional[list]
    reactions_emoticon_count_custom: Optional[int]
    reactions_doc_id_custom: Optional[list]
    reactions_doc_id_count_custom: Optional[int]

    @field_validator("ev_edit_date", mode="before")
    @classmethod
    def parse_ev_edit_date(cls, value: Any) -> datetime | None:
        if isinstance(value, datetime) or value is None:
            return value
        elif isinstance(value, str) and value == "":
            return None
        return datetime.fromisoformat(value)
