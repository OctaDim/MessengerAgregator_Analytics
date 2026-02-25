from datetime import datetime
from typing import Optional, Union, Literal, Self, Any

from pydantic import BaseModel, model_validator, field_validator


class BaseEventData(BaseModel):
    event_type: str
    web_account_id: str
    web_account_username: str
    tlt_account_type: str
    tlt_phone: Optional[str]
    tlt_bot_token: Optional[str]


class MewMessageData(BaseEventData):
    ev_message_message: Optional[str]
    ev_message_text: Optional[str]
    ev_message_raw_text: Optional[str]

    ev_original_update_pts: Optional[int]
    ev_original_update_pts_count: Optional[int]
    # ev__client:  # obj

    ev_id: Optional[int]

    # ev_peer_id: obj:
    ev_date: Optional[datetime]
    # ev_edit_date: Optional[datetime]
    ev_out: Optional[bool]
    ev_mentioned: Optional[bool]
    ev_media_unread: Optional[bool]
    ev_silent: Optional[bool]
    ev_post: Optional[bool]
    ev_from_scheduled: Optional[bool]
    ev_legacy: Optional[bool]
    ev_edit_hide: Optional[bool]
    ev_pinned: Optional[bool]
    ev_noforwards: Optional[bool]
    ev_invert_media: Optional[bool]
    ev_offline: Optional[bool]
    ev_video_processing_pending: Optional[bool]
    ev_paid_suggested_post_stars: Optional[bool]
    ev_paid_suggested_post_ton: Optional[bool]
    # ev_from_id:  # obj
    ev_from_boosts_applied: Optional[int]
    # ev_saved_peer_id:  # obj
    # ev_fwd_from: # obj
    ev_via_bot_id: Optional[bool]
    ev_via_business_bot_id: Optional[bool]
    # ev_reply_to:  # obj
    # ev_media:   # obj
    # ev_reply_markup:   # obj
    # ev_entities:   # list(objs)
    ev_views: Optional[list]  # = Field(default_factory=list)
    ev_forwards: Optional[list]  # = Field(default_factory=list)
    ev_replies: Optional[list]  # = Field(default_factory=list)
    ev_post_author: Optional[str]
    ev_grouped_id: Optional[int]
    ev_reactions: Optional[list]  # = Field(default_factory=list)
    ev_restriction_reason: Optional[list]  # = Field(default_factory=list)
    ev_ttl_period: Optional[int]
    ev_quick_reply_shortcut_id: Optional[int]
    ev_effect: Optional[int]
    # ev_factcheck:   # obj
    ev_report_delivery_until_date: Optional[datetime]
    # ev_paid_stars:   # obj
    # ev_suggested_post:   # obj

    # ev_file:   # obj
    ev_broadcast: Optional[bool]
    ev_is_reply: Optional[bool]
    ev_is_private: Optional[bool]
    ev_is_group: Optional[bool]
    ev_is_channel: Optional[bool]
    # ev_chat:  # obj
    ev_chat_id: Optional[int]
    # ev_chat__client:  # obj
    ev_sender_id: Optional[int]
    # ev_forward:  # obj
    # ev_photo  # obj
    # ev_document  # obj
    # ev_audio  # obj
    # ev_video  # obj
    # ev_voice  # obj
    # ev_sticker  # obj
    # ev_contact  # obj
    # ev_location  # obj
    # ev_venue  # obj
    # ev_game  # obj
    # ev_poll  # obj
    # ev_dice  # obj
    # ev_invoice  # obj
    # ev_web_preview  # obj
    # ev_action  # obj
    ev_changed_media: Optional[bool]
    ev_changed_text: Optional[bool]
    ev_changed_markup: Optional[bool]
    ev_changed_entities: Optional[bool]

    # peer_id options:
    ev_peer_id_channel_id: Optional[int]  # opt.1
    ev_peer_id_chat_id: Optional[int]  # opt.2
    ev_peer_id_user_id: Optional[int]  # opt.3

    # from_id options
    ev_from_id_channel_id: Optional[int]  # opt.1
    ev_from_id_chat_id: Optional[int]  # opt.2
    ev_from_id_user_id: Optional[int]  # opt.3

    ev_fwd_from_date: Optional[datetime]
    # ev_fwd_from_from_id:  # obj
    ev_fwd_from_from_name: Optional[str]
    ev_fwd_from_channel_post: Optional[int]
    ev_fwd_from_post_author: Optional[str]
    # ev_fwd_from_saved_from_peer:  # obj
    ev_fwd_from_saved_from_msg_id: Optional[int]

    # fwd_from_from_id options
    ev_fwd_from_from_id_channel_id: Optional[int]  # opt.1
    ev_fwd_from_from_id_chat_id: Optional[int]  # opt.2
    ev_fwd_from_from_id_user_id: Optional[int]  # opt.3

    ev_reply_to_reply_to_msg_id: Optional[int]
    # ev_reply_to_reply_to_peer_id:  # obj

    ev_reply_to_reply_to_top_id: Optional[int]
    ev_reply_to_reply_to_scheduled: Optional[bool]
    ev_reply_to_forum_topic: Optional[bool]
    ev_reply_to_quote: Optional[bool]
    ev_reply_to_quote_text: Optional[str]
    # ev_reply_to_reply_media:  # obj
    ev_reply_to_todo_item_id: Optional[int]

    ev_reply_to_reply_to_peer_id_channel_id: Optional[int]  # opt.1
    ev_reply_to_reply_to_peer_id_chat_id: Optional[int]  # opt.2
    ev_reply_to_reply_to_peer_id_user_id: Optional[int]  # opt.3

    # ev_media_photo:  # obj
    ev_media_photo_ttl_seconds: Optional[int]
    ev_media_photo_id: Optional[int]
    ev_media_photo_access_hash: Optional[int]
    ev_media_photo_file_reference: Optional[bytes]
    ev_media_photo_date: Optional[datetime]
    # ev_media_photo_sizes:  # objs
    # ev_media_video_sizes:  # objs
    ev_media_photo_has_stickers: Optional[bool]

    # ev_media_document:  # obj
    ev_media_document_ttl_seconds: Optional[int]
    ev_media_document_id: Optional[int]
    ev_media_document_access_hash: Optional[int]
    ev_media_document_file_reference: Optional[bytes]
    ev_media_document_date: Optional[datetime]
    ev_media_document_mime_type: Optional[str]
    ev_media_document_size: Optional[int]
    # ev_media_document_thumbs:  # objs
    # ev_media_document_video_thumbs:  # objs
    # ev_media_document_attributes:  # objs

    # ev_media_geo_geo:  # obj

    # ev_media_geo_live_geo:  # obj
    ev_media_heading: Optional[int]
    ev_media_period: Optional[int]
    ev_media_proximity_notification_radius: Optional[int]

    # ev_media_venue_geo:  # obj
    ev_media_title: Optional[str]
    ev_media_address: Optional[str]
    ev_media_provider: Optional[str]
    ev_media_venue_id: Optional[str]
    ev_media_venue_type: Optional[str]

    ev_media_phone_number: Optional[str]
    ev_media_first_name: Optional[str]
    ev_media_last_name: Optional[str]
    ev_media_vcard: Optional[str]

    # ev_media_poll:  # obj
    # ev_media_results:  # obj

    ev_media_value: Optional[int]
    ev_media_emoticon: Optional[str]

    # ev_media_game:  # obj
    # ev_media_invoice:  # obj
    # ev_media_webpage:  # obj

    ev_replies_replies: Optional[int]
    ev_replies_replies_pts: Optional[int]
    ev_replies_comments: Optional[bool]
    # ev_replies_recent_repliers:  # objs
    ev_replies_channel_id: Optional[int]  # opt.1
    ev_replies_max_id: Optional[int]
    ev_replies_read_max_id: Optional[int]

    ev_reactions_results: Optional[list]  # = Field(default_factory=list)
    ev_reactions_min: Optional[bool]
    ev_reactions_can_see_list: Optional[bool]
    ev_reactions_reactions_as_tags: Optional[bool]
    # ev_reactions_recent_reactions:  # objs
    # ev_reactions_top_reactors:  # objs

    ev_file_id: Optional[str]
    ev_file_name: Optional[str]
    ev_file_size: Optional[int]
    ev_file_date: Optional[datetime]
    ev_file_mime_type: Optional[str]

    ev_sender_username: Optional[str]
    ev_sender_first_name: Optional[str]
    ev_sender_last_name: Optional[str]
    ev_sender_bot: Optional[bool]

    @field_validator("ev_date", mode="before")
    @classmethod
    def parse_ev_date(cls, value: Any) -> datetime | None:
        if isinstance(value, datetime) or value is None:
            return value
        elif isinstance(value, str) and value == "":
            return None
        return datetime.fromisoformat(value)


class MessageEditedData(MewMessageData):  # Basically nested from MewMessageData
    ev_edit_date: Optional[datetime]

    @field_validator("ev_edit_date", mode="before")
    @classmethod
    def parse_ev_edit_date(cls, value: Any) -> datetime | None:
        if isinstance(value, datetime) or value is None:
            return value
        elif isinstance(value, str) and value == "":
            return None
        return datetime.fromisoformat(value)


class MessageReadData(BaseEventData):
    pass


class MessageDeletedData(BaseEventData):
    pass


class ChatActionData(BaseEventData):
    pass


class GlobalApiWebhookData(BaseModel):
    event_data: Optional[Union[
        MewMessageData, MessageEditedData, MessageReadData,
        MessageDeletedData, ChatActionData]]
    source: Optional[Union[str, Literal["tlt_tg_aggr"]]]
    operation: Optional[Union[str, Literal["test"]]]

    # # Validation in router to fix recursion error
    # def __init__(self, **data: Any) -> None:
    #     validate_log_pydantic_obj_errors(PydanticBaseModel=self.__class__,
    #                                      request_json=data)
    #     super().__init__(**data)

    @model_validator(mode="after")
    def validate_basemodel_obj(self) -> Self:
        # Validation in router to fix recursion error
        # validate_log_pydantic_obj_errors(PydanticBaseModel=self.__class__,
        #                                  request_json=self.model_dump())
        has_group_1_flag = all([self.event_data, self.source])
        has_group_2_flag = all([self.source, self.operation])
        if not (has_group_1_flag or has_group_2_flag):  # Both are False
            error_log = (
                f"PYDANTIC COMBINATIONS [ERROR]: "
                f"group 1 (event_data, source) OR "
                f"group 2 (source, operation) needed\n"
                f"has_group_1_flag: {has_group_1_flag}\n"
                f"has_group_2_flag: {has_group_1_flag}\n"
                f"\tevent_data: {self.event_data}\n"
                f"\tsource: {self.source}\n"
                f"\toperation: {self.operation}\n")
            print(error_log)
            raise ValueError(error_log)
        else:  # has_group_1_flag or has_group_2_flag
            return self
