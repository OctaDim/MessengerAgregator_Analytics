from datetime import datetime
from typing import Literal, Optional

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_base_event_data import (
    BaseEventData)


class MessageDeletedData(BaseEventData):
    event_type: Literal["MessageDeleted"]  # discriminator="MessageDeleted"

    ev_delete_date: Optional[datetime]

    ev_orig_upd_messages: Optional[list]  # = Field(default_factory=list)
    ev_orig_upd_pts: Optional[int]
    ev_orig_upd_pts_count: Optional[int]
    # ev__client:  # obj

    ev_deleted_id: Optional[int]
    ev_deleted_ids: Optional[list]  # = Field(default_factory=list)

    ev_is_private: Optional[bool]
    ev_is_group: Optional[bool]
    ev_is_channel: Optional[bool]
    # ev_chat:  # obj
    ev_chat_id: Optional[int]
    # ev_chat__client:  # obj
