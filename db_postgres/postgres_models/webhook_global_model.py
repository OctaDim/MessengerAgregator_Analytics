from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String, Text, JSON, BigInteger, LargeBinary, DateTime)
from sqlalchemy.orm import Mapped, mapped_column

from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_models.orm_models_fields_mixins import (
    ActiveMix, CreateUpdateMix)


class GlobalWebhookModel(Base, ActiveMix, CreateUpdateMix):
    __tablename__ = "webhook_global_api"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # ##################################################################
    # ######### COMFORTABLE VIEW FIELDS ORDER (start) ##################
    # ##################################################################
    event_type: Mapped[Optional[str]] = mapped_column(String(15))
    ev_chat_title: Mapped[Optional[str]]
    ev_message_message: Mapped[Optional[str]] = mapped_column(Text)
    ev_sender_username: Mapped[Optional[str]]
    ev_sender_first_name: Mapped[Optional[str]]
    ev_sender_last_name: Mapped[Optional[str]]
    ev_sender_bot: Mapped[Optional[bool]]
    ev_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ev_edit_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reactions_total_custom: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    reactions_total_count_custom: Mapped[Optional[int]]
    reactions_emoticon_custom: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    reactions_emoticon_count_custom: Mapped[Optional[int]]
    reactions_doc_id_custom: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    reactions_doc_id_count_custom: Mapped[Optional[int]]
    # ##################################################################
    # ########## COMFORTABLE VIEW FIELDS ORDER (end) ###################
    # ##################################################################

    # event_type: Mapped[Optional[str]] = mapped_column(String(15))  # Temporary changed order
    web_account_id: Mapped[Optional[str]] = mapped_column(String(10))
    web_account_username: Mapped[Optional[str]] = mapped_column(String(30))
    tlt_account_type: Mapped[Optional[str]] = mapped_column(String(10))
    tlt_phone: Mapped[Optional[str]] = mapped_column(String(30))
    tlt_bot_token: Mapped[Optional[str]] = mapped_column(String(15))

    # ev_message_message: Mapped[Optional[str]] = mapped_column(Text)  # Temporary changed order
    ev_message_text: Mapped[Optional[str]] = mapped_column(Text)
    ev_message_raw_text: Mapped[Optional[str]] = mapped_column(Text)

    ev_original_update_pts: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_original_update_pts_count: Mapped[Optional[int]]
    # ev__client:  # obj

    ev_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    # ev_peer_id: object:
    # ev_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)  # Temporary changed order
    # ev_edit_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)  # Temporary changed order

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
    ev_via_bot_id: Mapped[Optional[bool]] = mapped_column(BigInteger)
    ev_via_business_bot_id: Mapped[Optional[bool]] = mapped_column(BigInteger)
    # ev_reply_to:  # obj
    # ev_media:   # obj
    # ev_reply_markup:   # obj
    # ev_entities:   # list(objs)
    ev_views: Mapped[Optional[int]]
    ev_forwards: Mapped[Optional[int]]
    ev_replies: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # obj
    ev_post_author: Mapped[Optional[str]]
    ev_grouped_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    # ev_reactions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # list(objs)  >> custom
    ev_restriction_reason: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # obj
    ev_ttl_period: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_quick_reply_shortcut_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_effect: Mapped[Optional[int]]
    # ev_factcheck:   # obj
    ev_report_delivery_until_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
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

    ev_fwd_from_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
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

    ev_reply_to_reply_to_top_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_reply_to_reply_to_scheduled: Mapped[Optional[bool]]
    ev_reply_to_forum_topic: Mapped[Optional[bool]]
    ev_reply_to_quote: Mapped[Optional[bool]]
    ev_reply_to_quote_text: Mapped[Optional[str]]
    # ev_reply_to_reply_media:  # obj
    ev_reply_to_todo_item_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    ev_reply_to_reply_to_peer_id_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.1
    ev_reply_to_reply_to_peer_id_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.2
    ev_reply_to_reply_to_peer_id_user_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.3

    # ev_media_photo:  # obj
    ev_media_photo_ttl_seconds: Mapped[Optional[int]]
    ev_media_photo_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_media_photo_access_hash: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_media_photo_file_reference: Mapped[Optional[bytes]] = mapped_column(LargeBinary())
    ev_media_photo_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # ev_media_photo_sizes:  # objs
    # ev_media_video_sizes:  # objs
    ev_media_photo_has_stickers: Mapped[Optional[bool]]

    # ev_media_document:  # obj
    ev_media_document_ttl_seconds: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_media_document_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_media_document_access_hash: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_media_document_file_reference: Mapped[Optional[bytes]] = mapped_column(LargeBinary())
    ev_media_document_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ev_media_document_mime_type: Mapped[Optional[str]]
    ev_media_document_size: Mapped[Optional[int]]
    # ev_media_document_thumbs:  # objs
    # ev_media_document_video_thumbs:  # objs
    # ev_media_document_attributes:  # objs

    # ev_media_geo_geo:  # obj

    # ev_media_geo_live_geo:  # obj
    ev_media_heading: Mapped[Optional[int]]
    ev_media_period: Mapped[Optional[int]]
    ev_media_proximity_notification_radius: Mapped[Optional[int]]

    # ev_media_venue_geo:  # obj
    ev_media_title: Mapped[Optional[str]]
    ev_media_address: Mapped[Optional[str]]
    ev_media_provider: Mapped[Optional[str]]
    ev_media_venue_id: Mapped[Optional[str]]
    ev_media_venue_type: Mapped[Optional[str]]

    ev_media_phone_number: Mapped[Optional[str]]
    ev_media_first_name: Mapped[Optional[str]]
    ev_media_last_name: Mapped[Optional[str]]
    ev_media_vcard: Mapped[Optional[str]]

    # ev_media_poll:  # obj
    # ev_media_results:  # obj

    ev_media_value: Mapped[Optional[int]]
    ev_media_emoticon: Mapped[Optional[str]]

    # ev_media_game:  # obj
    # ev_media_invoice:  # obj
    # ev_media_webpage:  # obj

    ev_replies_replies: Mapped[Optional[int]]
    ev_replies_replies_pts: Mapped[Optional[int]]
    ev_replies_comments: Mapped[Optional[bool]]
    # ev_replies_recent_repliers:  # objs
    ev_replies_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # opt.1
    ev_replies_max_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ev_replies_read_max_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    ev_reactions_results: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # objs
    ev_reactions_min: Mapped[Optional[bool]]
    ev_reactions_can_see_list: Mapped[Optional[bool]]
    ev_reactions_reactions_as_tags: Mapped[Optional[bool]]
    # ev_reactions_recent_reactions:  # objs
    # ev_reactions_top_reactors:  # objs

    ev_file_id: Mapped[Optional[str]]
    ev_file_name: Mapped[Optional[str]]
    ev_file_size: Mapped[Optional[int]]
    ev_file_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ev_file_mime_type: Mapped[Optional[str]]

    # ev_sender_username: Mapped[Optional[str]]  # Temporary changed order
    # ev_sender_first_name: Mapped[Optional[str]]  # Temporary changed order
    # ev_sender_last_name: Mapped[Optional[str]]  # Temporary changed order
    # ev_sender_bot: Mapped[Optional[bool]]  # Temporary changed order

    # ev_chat_title: Mapped[Optional[str]]  # Temporary changed order

    # reactions_total_custom: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # Temporary changed order
    # reactions_total_count_custom: Mapped[Optional[int]]  # Temporary changed order
    # reactions_emoticon_custom: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # Temporary changed order
    # reactions_emoticon_count_custom: Mapped[Optional[int]]  # Temporary changed order
    # reactions_doc_id_custom: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # Temporary changed order
    # reactions_doc_id_count_custom: Mapped[Optional[int]]  # Temporary changed order
