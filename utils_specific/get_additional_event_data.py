from typing import Dict, Any

from sqlalchemy import Row

from configs.settings import GLOBAL_API_WEBHOOKS_OPTIONS
from utils_common.get_text_difference import get_text_difference_str


async def get_new_msg_addit_data(
        event_data_dict: Dict[str, str],
) -> Dict[str, str]:
    addit_data = {}
    addit_data.update({
        "username_cst": event_data_dict["tlt_sender_username"],
        "first_name_cst": event_data_dict["tlt_sender_first_name"],
        "last_name_cst": event_data_dict["tlt_sender_last_name"],
        "phone_cst": event_data_dict["tlt_sender_phone"],
        "bot_cst": event_data_dict["tlt_sender_bot"], })
    return addit_data


async def get_msg_edited_addit_data(
        pgs_object: Row[tuple[Any, ...]],
        event_data_dict: Dict[str, str],
) -> Dict[str, str]:
    addit_data = {}
    if pgs_object:
        addit_data.update({
            "old_message_message_cst": pgs_object.ev_message_message,
            "old_message_text_cst": pgs_object.ev_message_text,
            "old_message_raw_text_cst": pgs_object.ev_message_raw_text, })

    if event_data_dict:
        msg_difference_data = await get_text_difference_str(
            old_text=pgs_object.ev_message_message,
            new_text=event_data_dict["ev_message_message"],
            deleted_mark=GLOBAL_API_WEBHOOKS_OPTIONS.DELETED_DIFFERENCE_PART_STR,
            added_mark=GLOBAL_API_WEBHOOKS_OPTIONS.ADDED_DIFFERENCE_PART_STR,
            replaced_separator=GLOBAL_API_WEBHOOKS_OPTIONS.REPLACED_DIFFERENCE_SEPARATOR_STR,
            each_diff_separator=GLOBAL_API_WEBHOOKS_OPTIONS.DIFFERENCE_EACH_LINE_SEPARATOR_STR)
        msg_difference_str = msg_difference_data["all_changes_str"]

        addit_data.update({
            "message_difference": msg_difference_str,
            "ev_chat_title": event_data_dict["ev_chat_title"],
            "username_cst": event_data_dict["tlt_sender_username"],
            "first_name_cst": event_data_dict["tlt_sender_first_name"],
            "last_name_cst": event_data_dict["tlt_sender_last_name"],
            "phone_cst": event_data_dict["tlt_sender_phone"],
            "bot_cst": event_data_dict["tlt_sender_bot"], })

    if pgs_object.ev_chat_title != event_data_dict["ev_chat_title"]:
        addit_data.update({"old_chat_title_cst": pgs_object.ev_chat_title})
    return addit_data


async def get_msg_deleted_addit_data(
        pgs_object: Row[tuple[Any, ...]],
        event_data_dict: Dict[str, str],
) -> Dict[str, str]:
    addit_data = {}
    if pgs_object:
        addit_data.update({
            # "ev_chat_title": pgs_object.ev_chat_title,  # old_chat_title_cst used instead ev_chat_title

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
            "bot_cst": pgs_object.tlt_sender_bot, })

        addit_data.update({
            "old_chat_title_cst": pgs_object.ev_chat_title,
        })

        del_prefix = GLOBAL_API_WEBHOOKS_OPTIONS.DELETED_MESSAGE_PREFIX_STR
        pgs_msg_msg = pgs_object.ev_message_message
        pgs_msg_txt = pgs_object.ev_message_text
        pgs_msg_raw_txt = pgs_object.ev_message_raw_text
        pref_msg_msg = f"{del_prefix} {pgs_msg_msg}" if del_prefix else None
        pref_msg_txt = f"{del_prefix} {pgs_msg_txt}" if del_prefix else None
        pref_msg_raw_txt = f"{del_prefix} {pgs_msg_raw_txt}" if del_prefix else None
        addit_data.update({
            "ev_message_message": pref_msg_msg,
            "ev_message_text": pref_msg_txt,
            "ev_message_raw_text": pref_msg_raw_txt})

    # if pgs_object and event_data_dict:
    #     if pgs_object.ev_chat_title != event_data_dict["ev_chat_title"]:
    #         addit_data.update(
    #             {"old_chat_title_cst": pgs_object.ev_chat_title})
    return addit_data


async def get_msg_read_addit_data(
        pgs_object: Row[tuple[Any, ...]],
) -> Dict[str, str]:
    addit_data = {}
    if pgs_object:
        addit_data.update({
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
            "bot_cst": pgs_object.tlt_sender_bot, })
    return addit_data


async def get_chat_action_addit_data(
        pgs_object: Row[tuple[Any, ...]],
        event_data_dict: Dict[str, str],
) -> Dict[str, str] | dict:
    addit_data = {}
    if event_data_dict:
        addit_data.update({
            "username_cst": event_data_dict["user_username"],
            "first_name_cst": event_data_dict["user_first_name"],
            "last_name_cst": event_data_dict["user_last_name"],
            "phone_cst": event_data_dict["user_phone"],
            "bot_cst": event_data_dict["user_bot"], })

    if pgs_object and event_data_dict:
        if pgs_object.ev_chat_title != event_data_dict["ev_chat_title"]:
            addit_data.update(
                {"old_chat_title_cst": pgs_object.ev_chat_title})
    return addit_data


async def get_user_update_addit_data(
        event_data_dict: Dict[str, str],
) -> Dict[str, str]:
    addit_data = {}
    if event_data_dict:
        addit_data.update({
            "username_cst": event_data_dict["user_username"],
            "first_name_cst": event_data_dict["user_first_name"],
            "last_name_cst": event_data_dict["user_last_name"],
            "phone_cst": event_data_dict["user_phone"],
            "bot_cst": event_data_dict["user_bot"], })
    return addit_data
