from datetime import datetime
from typing import Literal, Optional

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_base_event_data import (
    BaseEventData)


class UserUpdateData(BaseEventData):
    event_type: Literal["UserUpdate"]  # discriminator="UserUpdate"

    ev_orig_upd_channel_id: Optional[int]
    ev_orig_upd_chat_id: Optional[int]
    ev_orig_upd_user_id: Optional[int]
    # ev_orig_upd_from_id:  # obj
    # ev_orig_upd_action:  # obj
    ev_orig_upd_top_msg_id: Optional[int]

    # ev__client:  # obj

    ev_user_id: Optional[int]
    # ev_status:  # obj
    ev_status_expires: Optional[datetime]
    ev_status_was_online: Optional[datetime]
    # ev_action:  # obj
    # ev_chat:  # ???
    # ev__chat:  # ???
    ev_chat_id: Optional[int]

    user_username: Optional[str] = None
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_phone: Optional[str] = None
    user_bot: Optional[bool] = None
