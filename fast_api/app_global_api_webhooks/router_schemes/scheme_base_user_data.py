from typing import Optional

from pydantic import BaseModel


class BaseUserData(BaseModel):
    user_id: Optional[int]
    user_is_self: Optional[bool]
    user_contact: Optional[bool]
    user_mutual_contact: Optional[bool]
    user_deleted: Optional[bool]
    user_bot: Optional[bool]
    user_bot_chat_history: Optional[bool]
    user_bot_nochats: Optional[bool]
    user_verified: Optional[bool]
    user_restricted: Optional[bool]
    user_min: Optional[bool]
    user_bot_inline_geo: Optional[bool]
    user_support: Optional[bool]
    user_scam: Optional[bool]
    user_apply_min_photo: Optional[bool]
    user_fake: Optional[bool]
    user_bot_attach_menu: Optional[bool]
    user_premium: Optional[bool]
    user_attach_menu_enabled: Optional[bool]
    user_bot_can_edit: Optional[bool]
    user_close_friend: Optional[bool]
    user_stories_hidden: Optional[bool]
    user_stories_unavailable: Optional[bool]
    user_contact_require_premium: Optional[bool]
    user_bot_business: Optional[bool]
    user_bot_has_main_app: Optional[bool]
    user_bot_forum_view: Optional[bool]
    user_access_hash: Optional[int]
    user_first_name: Optional[str]
    user_last_name: Optional[str]
    user_username: Optional[str]
    user_phone: Optional[str]
    user_bot_info_version: Optional[int]
    # user_restriction_reason:  # list(objs)
    user_bot_inline_placeholder: Optional[str]
    user_lang_code: Optional[str]
    # user_emoji_status:  # obj
    # user_usernames:  # list(objs)
    user_stories_max_id: Optional[int]
    # user_color:  # obj
    # user_profile_color  # obj
    user_bot_active_users: Optional[int]
    user_bot_verification_icon: Optional[int]
    user_send_paid_messages_stars: Optional[int]
