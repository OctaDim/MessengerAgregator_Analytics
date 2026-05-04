from typing import Dict

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from configs.settings import GLOBAL_API_OPTIONS
from db_postgres.postgres_models.webhook_global_model import (
    GlobalWebhookModel)
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_model_rows_flex_query)
from utils_common.serialize_custom_json import get_jsonable_value


async def get_paginated_messages_qry(
        ongoing_session: AsyncSession,
        web_account_id: str,
        web_account_username: str,
        current_page: int,
        messages_per_page: int,
) -> Dict[str, Dict[str, any]]:
    if not web_account_id or not web_account_username:
        return None

    filter_fields = {"web_account_id": web_account_id,
                     "web_account_username": web_account_username}

    try:
        result = await ongoing_session.execute(
            select(func.count(GlobalWebhookModel.id))
            .filter_by(**filter_fields))  # if only equal use filter_by, for any condition use where
        all_msgs_count = result.scalar()
        # result = await ongoing_session.execute(select(
        #     func.count(GlobalWebhookModel.id)))
        # all_msgs_count = result.scalar()

        paginated_msgs_data = []
        if current_page and messages_per_page:
            records_offset = (current_page - 1) * messages_per_page
        else:
            records_offset = None
        messages_objs = await get_model_rows_flex_query(
            orm_model_class=GlobalWebhookModel,
            ongoing_session=ongoing_session,
            selected_fields=None,
            fields_values_filter=filter_fields,
            order_by_fields=GlobalWebhookModel.id.desc(),
            records_limit=messages_per_page,
            records_offset=records_offset,
            return_scalars=True)

        if messages_objs:
            log_non_jsonable_value = GLOBAL_API_OPTIONS.LOG_NON_JSONABLE_VALUE_ERROR
            for cur_msg_obj in messages_objs:
                ev_date_jsonable = await get_jsonable_value(
                    orig_obj_value=cur_msg_obj.ev_date,
                    obj_log_name="ev_date",
                    log_invalid_json=log_non_jsonable_value)
                ev_edit_date_jsonable = await get_jsonable_value(
                    orig_obj_value=cur_msg_obj.ev_edit_date,
                    obj_log_name="ev_edit_date",
                    log_invalid_json=log_non_jsonable_value)
                ev_delete_date_jsonable = await get_jsonable_value(
                    orig_obj_value=cur_msg_obj.ev_delete_date,
                    obj_log_name="ev_delete_date",
                    log_invalid_json=log_non_jsonable_value)

                cur_msg_data = {
                    "id": cur_msg_obj.id,
                    "action": cur_msg_obj.action,
                    "ev_id": cur_msg_obj.ev_id,  # Used for getting file
                    "ev_chat_title": cur_msg_obj.ev_chat_title,
                    "old_chat_title_cst": cur_msg_obj.old_chat_title_cst,
                    "ev_message_message": cur_msg_obj.ev_message_message,
                    "old_message_message_cst": cur_msg_obj.old_message_message_cst,
                    "message_difference": cur_msg_obj.message_difference,
                    "ev_sender_id": cur_msg_obj.ev_sender_id,
                    "ev_from_id_user_id":  cur_msg_obj.ev_from_id_user_id,
                    "ev_peer_id_channel_id": cur_msg_obj.ev_peer_id_channel_id,  # Used for getting file
                    "ev_peer_id_chat_id": cur_msg_obj.ev_peer_id_chat_id,  # Used for getting file
                    "ev_peer_id_user_id": cur_msg_obj.ev_peer_id_user_id,  # Used for getting file
                    "username_cst": cur_msg_obj.username_cst,
                    "first_name_cst": cur_msg_obj.first_name_cst,
                    "last_name_cst": cur_msg_obj.last_name_cst,
                    "phone_cst": cur_msg_obj.phone_cst,
                    "bot_cst": cur_msg_obj.bot_cst,
                    "file_name_cst": cur_msg_obj.file_name_cst,
                    "extra_file_name_cst": cur_msg_obj.extra_file_name_cst,
                    "tlt_config_name": cur_msg_obj.tlt_config_name,
                    # "telethon_config_name": cur_msg_obj.telethon_config_name,
                    "tlt_sender_username": cur_msg_obj.tlt_sender_username,
                    "tlt_sender_first_name": cur_msg_obj.tlt_sender_first_name,
                    "tlt_sender_last_name": cur_msg_obj.tlt_sender_last_name,
                    "tlt_sender_phone": cur_msg_obj.tlt_sender_phone,
                    "tlt_sender_bot": cur_msg_obj.tlt_sender_bot,
                    "ev_date": ev_date_jsonable[1],
                    "ev_edit_date": ev_edit_date_jsonable[1],
                    "ev_delete_date": ev_delete_date_jsonable[1],
                    "reactions_total_cst": cur_msg_obj.reactions_total_cst,
                    "reactions_total_count_cst": cur_msg_obj.reactions_total_count_cst,
                    "reactions_emoticon_cst": cur_msg_obj.reactions_emoticon_cst,
                    "reactions_emoticon_count_cst": cur_msg_obj.reactions_emoticon_count_cst,
                    "tlt_account_type": cur_msg_obj.tlt_account_type,
                    "tlt_phone": cur_msg_obj.tlt_phone,
                    "tlt_bot_token": cur_msg_obj.tlt_bot_token,
                    "ev_out": cur_msg_obj.ev_out,
                    "ev_chat_id": cur_msg_obj.ev_chat_id,
                }
                paginated_msgs_data.append(cur_msg_data)
        paginated_msgs_details = {
            "paginated_messages": paginated_msgs_data,
            "all_messages_count": all_msgs_count}
        return paginated_msgs_details
    except Exception as error:
        log_text = (f"Getting paginated messages data [ERROR]:\n"
                    f"error: {error}\n"
                    f"orm_model_class: {GlobalWebhookModel}\n"
                    f"current_page: {current_page}\n"
                    f"messages_per_page: {messages_per_page}\n")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
