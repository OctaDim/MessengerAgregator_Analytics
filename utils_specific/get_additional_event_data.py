from typing import Dict, Any

from sqlalchemy import Row

from configs.settings import GLOBAL_API_WEBHOOKS_OPTIONS


async def get_new_msg_addit_data(
        event_data_dict: Dict[str, str],
        event_type: str
) -> Dict[str, str]:
    addit_data = {
        "username_cst": event_data_dict["tlt_sender_username"],
        "first_name_cst": event_data_dict["tlt_sender_first_name"],
        "last_name_cst": event_data_dict["tlt_sender_last_name"],
        "phone_cst": event_data_dict["tlt_sender_phone"],
        "bot_cst": event_data_dict["tlt_sender_bot"], }
    return addit_data


async def get_msg_edited_addit_data(
        pgs_object: Row[tuple[Any, ...]],
        event_data_dict: Dict[str, str],
        event_type: str
) -> Dict[str, str]:
    addit_data = {
        "ev_chat_title": event_data_dict["ev_chat_title"],

        "old_message_message_cst": pgs_object.ev_message_message,
        "old_message_text_cst": pgs_object.ev_message_text,
        "old_message_raw_text_cst": pgs_object.ev_message_raw_text,

        "username_cst": event_data_dict["tlt_sender_username"],
        "first_name_cst": event_data_dict["tlt_sender_first_name"],
        "last_name_cst": event_data_dict["tlt_sender_last_name"],
        "phone_cst": event_data_dict["tlt_sender_phone"],
        "bot_cst": event_data_dict["tlt_sender_bot"], }

    if pgs_object.ev_chat_title != event_data_dict["ev_chat_title"]:
        addit_data.update({"old_chat_title_cst": pgs_object.ev_chat_title})
    return addit_data


async def get_msg_deleted_addit_data(
        pgs_object: Row[tuple[Any, ...]],
        event_type: str
) -> Dict[str, str]:
    addit_data = {
        "ev_chat_title": pgs_object.ev_chat_title,

        # "ev_message_message": pgs_object.ev_message_message,
        # "ev_message_text": pgs_object.ev_message_text,
        # "ev_message_raw_text": pgs_object.ev_message_raw_text,

        "old_message_message_cst": pgs_object.ev_message_message,
        "old_message_text_cst": pgs_object.ev_message_text,
        "old_message_raw_text_cst": pgs_object.ev_message_raw_text,

        "tlt_sender_username": pgs_object.tlt_sender_username,
        "tlt_sender_first_name": pgs_object.tlt_sender_first_name,
        "tlt_sender_last_name": pgs_object.tlt_sender_last_name,
        "tlt_sender_bot": pgs_object.tlt_sender_bot,

        "username_cst": pgs_object.tlt_sender_username,
        "first_name_cst": pgs_object.tlt_sender_first_name,
        "last_name_cst": pgs_object.tlt_sender_last_name,
        "phone_cst": pgs_object.tlt_sender_phone,
        "bot_cst": pgs_object.tlt_sender_bot, }

    del_prefix = GLOBAL_API_WEBHOOKS_OPTIONS.DELETED_MESSAGE_PREFIX_STR
    ev_msg_msg = pgs_object.ev_message_message
    ev_msg_txt = pgs_object.ev_message_text
    ev_msg_raw_txt = pgs_object.ev_message_raw_text
    del_msg_msg = f"{del_prefix} {ev_msg_msg}" if del_prefix else None
    del_msg_txt = f"{del_prefix} {ev_msg_txt}" if del_prefix else None
    del_msg_raw_txt = f"{del_prefix} {ev_msg_raw_txt}" if del_prefix else None
    addit_data.update({"ev_message_message": del_msg_msg,
                       "ev_message_text": del_msg_txt,
                       "ev_message_raw_text": del_msg_raw_txt})
    return addit_data


async def get_msg_read_addit_data(
        pgs_object: Row[tuple[Any, ...]],
        event_type: str
) -> Dict[str, str]:
    addit_data = {
        "ev_chat_title": pgs_object.ev_chat_title,

        "ev_message_message": pgs_object.ev_message_message,
        "ev_message_text": pgs_object.ev_message_text,
        "ev_message_raw_text": pgs_object.ev_message_raw_text,

        "tlt_sender_username": pgs_object.tlt_sender_username,
        "tlt_sender_first_name": pgs_object.tlt_sender_first_name,
        "tlt_sender_last_name": pgs_object.tlt_sender_last_name,
        "tlt_sender_bot": pgs_object.tlt_sender_bot,

        "username_cst": pgs_object.tlt_sender_username,
        "first_name_cst": pgs_object.tlt_sender_first_name,
        "last_name_cst": pgs_object.tlt_sender_last_name,
        "phone_cst": pgs_object.tlt_sender_phone,
        "bot_cst": pgs_object.tlt_sender_bot, }
    return addit_data


async def get_chat_action_addit_data(
        pgs_object: Row[tuple[Any, ...]],
        event_data_dict: Dict[str, str],
        event_type: str
) -> Dict[str, str] | dict:
    if pgs_object.ev_chat_title != event_data_dict["ev_chat_title"]:
        return {"old_chat_title_cst": pgs_object.ev_chat_title}
    return {}
