from datetime import datetime
from typing import Literal, Optional, Any

from pydantic import field_validator

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_base_event_data import (
    BaseEventData)


class ChatActionData(BaseEventData):
    event_type: Literal["ChatAction"]  # discriminator="ChatAction"

    ev_orig_upd_pts: Optional[int]
    ev_orig_upd_pts_count: Optional[int]
    # ev__client:  # obj

    ev_new_pin: Optional[bool]
    ev_new_photo: Optional[bool]
    # ev_photo:  # obj
    ev_user_added: Optional[bool]
    ev_user_joined: Optional[bool]
    ev_user_left: Optional[bool]
    ev_user_kicked: Optional[bool]
    ev_unpin: Optional[bool]
    ev_created: Optional[bool]
    ev_new_title: Optional[str]
    ev_new_score: Optional[int]
    ev_act_msg_id: Optional[int]
    ev_act_msg_date: Optional[datetime]
    ev_act_msg_action_users: Optional[list]  # opt.1
    ev_act_msg_action_user_id: Optional[int]  # opt.2
    ev_act_msg_out: Optional[bool]
    ev_act_msg_mentioned: Optional[bool]
    ev_act_msg_media_unread: Optional[bool]
    ev_act_msg_reactions_are_possible: Optional[bool]
    ev_act_msg_silent: Optional[bool]
    ev_act_msg_post: Optional[bool]
    ev_act_msg_legacy: Optional[bool]
    # ev_act_msg_saved_peer_id:  # obj
    # ev_act_msg_reactions:  # obj
    ev_act_msg_ttl_period: Optional[int]

    ev_act_msg_peer_id_channel_id: Optional[int]  # opt.1
    ev_act_msg_peer_id_chat_id: Optional[int]  # opt.2
    ev_act_msg_peer_id_user_id: Optional[int]  # opt.3

    ev_act_msg_from_id_channel_id: Optional[int]  # opt.1
    ev_act_msg_from_id_chat_id: Optional[int]  # opt.2
    ev_act_msg_from_id_user_id: Optional[int]  # opt.3

    ev_act_msg_saved_peer_id_channel_id: Optional[int]  # opt.1
    ev_act_msg_saved_peer_id_chat_id: Optional[int]  # opt.2
    ev_act_msg_saved_peer_id_user_id: Optional[int]  # opt.3

    ev_orig_upd_message_action_users: Optional[list]  # opt.1
    ev_orig_upd_message_action_user_id: Optional[int]  # opt.2

    ev_is_private: Optional[bool]
    ev_is_group: Optional[bool]
    ev_is_channel: Optional[bool]
    ev_chat_id: Optional[int]

    ev_chat_id: Optional[int]
    ev_chat_title: Optional[str]

    user_username: Optional[str]
    user_first_name: Optional[str]
    user_last_name: Optional[str]
    user_phone: Optional[str]
    user_bot: Optional[bool]

    @field_validator("ev_act_msg_date", mode="before")
    @classmethod
    def parse_ev_act_msg_date(cls, value: Any) -> datetime | None:
        if isinstance(value, datetime) or value is None:
            return value
        elif isinstance(value, str) and value == "":
            return None
        return datetime.fromisoformat(value)
