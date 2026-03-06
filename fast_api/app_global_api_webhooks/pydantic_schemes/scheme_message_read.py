from typing import Literal, Optional

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_base_event_data import (
    BaseEventData)


class MessageReadData(BaseEventData):
    event_type: Literal["MessageRead"]  # discriminator="MessageRead"

    ev_orig_upd_pts: Optional[int]
    ev_orig_upd_pts_count: Optional[int]
    # ev__client:  # obj

    ev_outbox: Optional[bool]
    ev_contents: Optional[bool]
    ev_max_id: Optional[int]

    ev_is_private: Optional[bool]
    ev_is_group: Optional[bool]
    ev_is_channel: Optional[bool]
    # ev_chat:  # obj
    ev_chat_id: Optional[int]
    # ev_chat__client:  # obj

    ev_orig_upd_peer_channel_id: Optional[int]
    ev_orig_upd_peer_chat_id: Optional[int]
    ev_orig_upd_peer_user_id: Optional[int]
