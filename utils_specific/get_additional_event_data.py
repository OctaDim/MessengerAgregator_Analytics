from typing import Dict, Any

from sqlalchemy import Row


async def get_msg_deleted_event_add_data(
        pgs_message_obj: Row[tuple[Any, ...]],
        event_type: str
) -> Dict[str, str]:
    pgs_msg_msg = pgs_message_obj.ev_message_message
    pgs_msg_txt = pgs_message_obj.ev_message_text
    pgs_raw_txt = pgs_message_obj.ev_message_raw_text
    pgs_chat_title = pgs_message_obj.ev_chat_title
    pgs_sndr_username = pgs_message_obj.ev_sender_username
    pgs_sndr_first_name = pgs_message_obj.ev_sender_first_name
    pgs_sndr_last_name = pgs_message_obj.ev_sender_last_name
    pgs_sndr_bot = pgs_message_obj.ev_sender_bot
    additional_data = {
        "ev_message_message": pgs_msg_msg,
        "ev_message_text": pgs_msg_txt,
        "ev_message_raw_text": pgs_raw_txt,
        "ev_chat_title": pgs_chat_title,
        "ev_sender_username": pgs_sndr_username,
        "ev_sender_first_name": pgs_sndr_first_name,
        "ev_sender_last_name": pgs_sndr_last_name,
        "ev_sender_bot": pgs_sndr_bot, }
    return additional_data


async def get_msg_read_event_add_data(
        pgs_message_obj: Row[tuple[Any, ...]],
        event_type: str
) -> Dict[str, str]:
    pgs_msg_msg = pgs_message_obj.ev_message_message
    pgs_msg_txt = pgs_message_obj.ev_message_text
    pgs_raw_txt = pgs_message_obj.ev_message_raw_text
    pgs_chat_title = pgs_message_obj.ev_chat_title
    pgs_sndr_username = pgs_message_obj.ev_sender_username
    pgs_sndr_first_name = pgs_message_obj.ev_sender_first_name
    pgs_sndr_last_name = pgs_message_obj.ev_sender_last_name
    pgs_sndr_bot = pgs_message_obj.ev_sender_bot
    additional_data = {
        "ev_message_message": pgs_msg_msg,
        "ev_message_text": pgs_msg_txt,
        "ev_message_raw_text": pgs_raw_txt,
        "ev_chat_title": pgs_chat_title,
        "ev_sender_username": pgs_sndr_username,
        "ev_sender_first_name": pgs_sndr_first_name,
        "ev_sender_last_name": pgs_sndr_last_name,
        "ev_sender_bot": pgs_sndr_bot, }
    return additional_data


async def get_chat_action_event_add_data(
        pgs_message_obj: Row[tuple[Any, ...]],
        event_type: str
) -> Dict[str, str]:
    pgs_ev_chat_title = pgs_message_obj.ev_chat_title
    additional_data = {
        "old_chat_title_custom": pgs_ev_chat_title, }
    return additional_data
