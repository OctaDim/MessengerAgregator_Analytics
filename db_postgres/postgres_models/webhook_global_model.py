from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String, Text, JSON, BigInteger, ForeignKey, TIMESTAMP, LargeBinary)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, LocalCreateUpdateMix, CreateUpdateMix)


class GlobalWebhookMsgModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "api_global_webhook_message"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    event_type: Mapped[Optional[str]] = mapped_column(String(15))
    web_account_id: Mapped[Optional[str]] = mapped_column(String(10))
    web_account_username: Mapped[Optional[str]] = mapped_column(String(30))
    tlt_account_type: Mapped[Optional[str]] = mapped_column(String(10))
    tlt_phone: Mapped[Optional[str]] = mapped_column(String(30))
    tlt_bot_token: Mapped[Optional[str]] = mapped_column(String(15))

    ev_message_message: Mapped[Optional[str]] = mapped_column(Text)
    ev_message_text: Mapped[Optional[str]] = mapped_column(Text)
    ev_message_raw_text: Mapped[Optional[str]] = mapped_column(Text)

    ev_original_update_pts: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_original_update_pts_count: Mapped[Optional[int]]
    # ev__client:  # obj

    ev_id: Mapped[Optional[int]]

    # ev_peer_id: object:
    ev_date: Mapped[Optional[datetime]]
    ev_edit_date: Mapped[Optional[datetime]]
    ev_out: Mapped[Optional[bool]]
    ev_mentioned: Mapped[Optional[bool]]
    ev_media_unread: Mapped[Optional[bool]]
    ev_silent: Mapped[Optional[bool]]
    ev_post: Mapped[Optional[bool]]
    ev_from_scheduled: Mapped[Optional[bool]]
    ev_legacy: Mapped[Optional[bool]]
    ev_edit_hide: Mapped[Optional[bool]]
    ev_pinned: Mapped[Optional[bool]]
    ev_noforwards: Mapped[Optional[bool]]
    ev_invert_media: Mapped[Optional[bool]]
    ev_offline: Mapped[Optional[bool]]
    ev_video_processing_pending: Mapped[Optional[bool]]
    ev_paid_suggested_post_stars: Mapped[Optional[bool]]
    ev_paid_suggested_post_ton: Mapped[Optional[bool]]
    # ev_from_id:  # obj
    ev_from_boosts_applied: Mapped[Optional[int]]
    # ev_saved_peer_id:  # obj
    # ev_fwd_from: # obj
    ev_via_bot_id: Mapped[Optional[bool]]
    ev_via_business_bot_id: Mapped[Optional[bool]]
    # ev_reply_to:  # obj
    # ev_media:   # obj
    # ev_reply_markup:   # obj
    # ev_entities:   # list(objs)
    # ev_views: # obj
    # ev_forwards: # obj
    # ev_replies:   # obj
    ev_post_author: Mapped[Optional[str]]
    ev_grouped_id: Mapped[Optional[int]]
    # ev_reactions:   # obj
    # ev_restriction_reason:   # list(objs)
    ev_ttl_period: Mapped[Optional[int]]
    ev_quick_reply_shortcut_id: Mapped[Optional[int]]
    ev_effect: Mapped[Optional[int]]
    # ev_factcheck:   # obj
    ev_report_delivery_until_date: Mapped[Optional[datetime]]
    # ev_paid_stars:   # obj
    # ev_suggested_post:   # obj

    # ev_file:   # obj
    ev_broadcast: Mapped[Optional[bool]]
    ev_is_reply: Mapped[Optional[bool]]
    ev_is_private: Mapped[Optional[bool]]
    ev_is_group: Mapped[Optional[bool]]
    ev_is_channel: Mapped[Optional[bool]]
    # ev_chat:  # obj
    ev_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # ev_chat__client:  # obj
    ev_sender_id: Mapped[Optional[int]] = mapped_column(BigInteger)
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
    ev_changed_media: Mapped[Optional[bool]]
    ev_changed_text: Mapped[Optional[bool]]
    ev_changed_markup: Mapped[Optional[bool]]
    ev_changed_entities: Mapped[Optional[bool]]

    # peer_id options:
    ev_peer_id_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.1
    ev_peer_id_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.2
    ev_peer_id_user_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.3

    # from_id options
    ev_from_id_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.1
    ev_from_id_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.2
    ev_from_id_user_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.3

    ev_fwd_from_date: Mapped[Optional[datetime]]
    # ev_fwd_from_from_id:  # obj
    ev_fwd_from_from_name: Mapped[Optional[str]]
    ev_fwd_from_channel_post: Mapped[Optional[int]]
    ev_fwd_from_post_author: Mapped[Optional[str]]
    # ev_fwd_from_saved_from_peer:  # obj
    ev_fwd_from_saved_from_msg_id: Mapped[Optional[int]]

    # fwd_from_from_id options
    ev_fwd_from_from_id_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.1
    ev_fwd_from_from_id_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.2
    ev_fwd_from_from_id_user_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.3

    ev_reply_to_reply_to_msg_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # ev_reply_to_reply_to_peer_id:  # obj

    ev_reply_to_reply_to_top_id: Mapped[Optional[int]]
    ev_reply_to_reply_to_scheduled: Mapped[Optional[bool]]
    ev_reply_to_forum_topic: Mapped[Optional[bool]]
    ev_reply_to_quote: Mapped[Optional[bool]]
    ev_reply_to_quote_text: Mapped[Optional[str]]
    # ev_reply_to_reply_media:  # obj
    ev_reply_to_todo_item_id: Mapped[Optional[int]]

    ev_reply_to_reply_to_peer_id_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.1
    ev_reply_to_reply_to_peer_id_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.2
    ev_reply_to_reply_to_peer_id_user_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.3

    ev_media_photo ==
    ev_media_photo_ttl_seconds ==
    ev_media_photo_id ==
    ev_media_photo_access_hash ==
    ev_media_photo_file_reference ==
    ev_media_photo_date ==
    ev_media_photo_sizes ==
    ev_media_photo_has_stickers ==

    ev_media_document ==
    ev_media_document_ttl_seconds ==
    ev_media_document_id ==
    ev_media_document_access_hash ==
    ev_media_document_file_reference ==
    ev_media_document_date ==
    ev_media_document_mime_type ==
    ev_media_document_size ==
    ev_media_document_thumbs ==
    ev_media_document_video_thumbs ==
    ev_media_document_attributes ==
    ev_media_document_ ==

    ev_media_geo_geo ==

    ev_media_geo_live_geo ==
    ev_media_heading ==
    ev_media_period ==
    ev_media_proximity_notification_radius ==

    ev_media_venue_geo ==
    ev_media_title ==
    ev_media_address ==
    ev_media_provider ==
    ev_media_venue_id ==
    ev_media_venue_type ==

    ev_media_phone_number ==
    ev_media_first_name ==
    ev_media_last_name ==
    ev_media_vcard ==

    ev_media_poll ==
    ev_media_results ==

    ev_media_value ==
    ev_media_emoticon ==

    ev_media_game ==

    ev_media_invoice ==

    ev_media_webpage ==

    ev_replies_replies ==
    ev_replies_comments ==
    ev_replies_recent_repliers ==
    ev_replies_channel_id ==
    ev_replies_max_id ==
    ev_replies_read_max_id ==

    ev_reactions_results ==
    ev_reactions_min ==
    ev_reactions_can_see_list ==
    ev_reactions_reactions_as_tags ==
    ev_reactions_recent_reactions ==
    ev_reactions_top_reactors ==

    ev_file_id ==
    ev_file_name ==
    ev_file_size ==
    ev_file_date ==
    ev_file_mime_type ==

    ev_sender_username == DimaMezhevich( <

    class 'str'> )
    ev_sender_first_name == Dima ( < class 'str' > )
    ev_sender_last_name == Mezhevich ( < class 'str' > )
    ev_sender_bot == False ( < class 'bool' > )
















    ev_media_photo_ttl_seconds: Mapped[Optional[int]]
    ev_media_photo_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_media_photo_access_hash: Mapped[Optional[int]]
    ev_media_photo_file_reference: Mapped[Optional[bytes]] = mapped_column(LargeBinary())
    ev_media_photo_date: Mapped[Optional[datetime]]
    # ev_media_photo_sizes  # object


    # event_message_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # event_message_date: Mapped[Optional[datetime]]
    # event_message_edit_date: Mapped[Optional[datetime]]
    # event_message_file: Mapped[Optional[str]]
    # event_message_out: Mapped[Optional[bool]]
    # event_message_is_reply: Mapped[Optional[bool]]
    # event_message_is_private: Mapped[Optional[bool]]
    # event_message_is_group: Mapped[Optional[bool]]
    # event_message_is_channel: Mapped[Optional[bool]]
    # event_message_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # event_message_sender_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # event_message_message_id:


    # external_id: Mapped[Optional[str]]
    # company_id: Mapped[Optional[int]]
    # conversation_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # contact_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # replied_to_id: Mapped[Optional[int]]
    # income: Mapped[Optional[bool]]
    # status: Mapped[Optional[str]] = mapped_column(String(15))
    # message: Mapped[Optional[str]] = mapped_column(Text)
    # reactions: Mapped[Optional[list]] = mapped_column(JSON)  # JSON
    # details: Mapped[Optional[list]] = mapped_column(JSON)  # JSON
    # attachments: Mapped[Optional[list]] = mapped_column(JSON)  # JSON
    # delivery: Mapped[Optional[bool]] = mapped_column(default=False)
    # deleted: Mapped[Optional[bool]] = mapped_column(default=False)
    #
    # created_at: Mapped[Optional[datetime]] = mapped_column(
    #     TIMESTAMP(timezone=True))
    # external_created_at: Mapped[Optional[datetime]] = mapped_column(
    #     TIMESTAMP(timezone=True))
    #
    # provider: Mapped[Optional[str]] = mapped_column(String(30))
    # sender_name: Mapped[Optional[str]]
    # file_name: Mapped[Optional[str]] = mapped_column(String(255))
    # mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    # push_to_talk: Mapped[Optional[bool]] = mapped_column(default=False)
    # attachment_url: Mapped[Optional[str]] = mapped_column(String(255))
    # emoji_count: Mapped[Optional[int]]
    # webp_count: Mapped[Optional[int]]
    #
    # @hybrid_property
    # def pty_file_name(self):
    #     valid_attachment_flag = all(
    #         [self.attachments, isinstance(self.attachments, list)])
    #     if valid_attachment_flag:
    #         property_value = self.attachments[0].get("file_name")
    #         return property_value
    #     else:
    #         return None
    #
    # @hybrid_property
    # def pty_mime_type(self):
    #     valid_attachment_flag = all([self.attachments,
    #                                  isinstance(self.attachments, list)])
    #     if valid_attachment_flag:
    #         property_value = self.attachments[0].get("mime_type")
    #         return property_value
    #     else:
    #         return None
    #
    # @hybrid_property
    # def pty_push_to_talk(self):
    #     valid_attachment_flag = all([self.attachments,
    #                                  isinstance(self.attachments, list)])
    #     if valid_attachment_flag:
    #         property_value = self.attachments[0].get("push_to_talk")
    #         return property_value
    #     else:
    #         return None
    #
    # @hybrid_property
    # def pty_attachment_url(self):
    #     valid_attachment_flag = all([self.attachments,
    #                                  isinstance(self.attachments, list)])
    #     if valid_attachment_flag:
    #         property_value = self.attachments[0].get("attachment_url")
    #         return property_value
    #     else:
    #         return None

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
