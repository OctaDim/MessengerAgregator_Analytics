from typing import Dict

from fastapi import HTTPException
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from configs.settings import GLOBAL_API_OPTIONS
from db_postgres.postgres_models.webhook_global_model import (
    GlobalWebhookModel)
from fast_api.app_get_paginated_messages_by_contacts.scheme_messages_by_contacts import (
    InTelegramContactData)
from utils_common.serialize_custom_json import get_jsonable_value


async def _serialize_global_webhook_message_obj(
        cur_msg_obj: GlobalWebhookModel) -> Dict[str, any]:
    log_non_jsonable_value = GLOBAL_API_OPTIONS.LOG_NON_JSONABLE_VALUE_ERROR
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
        "ev_id": cur_msg_obj.ev_id,
        "ev_chat_title": cur_msg_obj.ev_chat_title,
        "old_chat_title_cst": cur_msg_obj.old_chat_title_cst,
        "ev_message_message": cur_msg_obj.ev_message_message,
        "old_message_message_cst": cur_msg_obj.old_message_message_cst,
        "message_difference": cur_msg_obj.message_difference,
        "ev_sender_id": cur_msg_obj.ev_sender_id,
        "ev_from_id_user_id": cur_msg_obj.ev_from_id_user_id,
        "ev_peer_id_channel_id": cur_msg_obj.ev_peer_id_channel_id,
        "ev_peer_id_chat_id": cur_msg_obj.ev_peer_id_chat_id,
        "ev_peer_id_user_id": cur_msg_obj.ev_peer_id_user_id,
        "username_cst": cur_msg_obj.username_cst,
        "first_name_cst": cur_msg_obj.first_name_cst,
        "last_name_cst": cur_msg_obj.last_name_cst,
        "phone_cst": cur_msg_obj.phone_cst,
        "bot_cst": cur_msg_obj.bot_cst,
        "file_name_cst": cur_msg_obj.file_name_cst,
        "extra_file_name_cst": cur_msg_obj.extra_file_name_cst,
        "tlt_config_name": cur_msg_obj.tlt_config_name,
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
        "s3_bucket": cur_msg_obj.s3_bucket,
        "s3_key": cur_msg_obj.s3_key,
        "s3_endpoint": cur_msg_obj.s3_endpoint,
        "s3_uri": cur_msg_obj.s3_uri,
    }
    return cur_msg_data


def _create_contact_where_conditions(
        telegram_contacts: list[InTelegramContactData]) -> list:
    contact_where_conditions = []
    for cur_contact in telegram_contacts:
        one_contact_where = []
        if cur_contact.username_cst:
            one_contact_where.append(
                GlobalWebhookModel.username_cst == cur_contact.username_cst)
        if cur_contact.phone_cst:
            one_contact_where.append(
                GlobalWebhookModel.phone_cst == cur_contact.phone_cst)
        if cur_contact.first_name_cst:
            one_contact_where.append(
                GlobalWebhookModel.first_name_cst == cur_contact.first_name_cst)
        if cur_contact.last_name_cst:
            one_contact_where.append(
                GlobalWebhookModel.last_name_cst == cur_contact.last_name_cst)
        if one_contact_where:
            contact_where_conditions.append(and_(*one_contact_where))
    return contact_where_conditions


async def get_paginated_messages_by_contacts_qry(
        ongoing_session: AsyncSession,
        web_account_id: str,
        web_account_username: str,
        telegram_contacts: list[InTelegramContactData],
        current_page: int,
        messages_per_page: int,
        tlt_config_name: str | None = None,
) -> Dict[str, Dict[str, any]]:
    if not web_account_id or not web_account_username or not telegram_contacts:
        return None

    try:
        base_where_conditions = [
            GlobalWebhookModel.web_account_id == web_account_id,
            GlobalWebhookModel.web_account_username == web_account_username,
        ]
        if tlt_config_name:
            base_where_conditions.append(
                GlobalWebhookModel.tlt_config_name == tlt_config_name)

        contact_where_conditions = _create_contact_where_conditions(
            telegram_contacts=telegram_contacts)
        full_where_condition = and_(
            *base_where_conditions,
            or_(*contact_where_conditions))

        result = await ongoing_session.execute(
            select(func.count(GlobalWebhookModel.id)).where(
                full_where_condition))
        all_msgs_count = result.scalar()

        if current_page and messages_per_page:
            records_offset = (current_page - 1) * messages_per_page
        else:
            records_offset = None

        messages_result = await ongoing_session.execute(
            select(GlobalWebhookModel)
            .where(full_where_condition)
            .order_by(GlobalWebhookModel.id.desc())
            .limit(messages_per_page)
            .offset(records_offset))
        messages_objs = messages_result.scalars().all()

        paginated_msgs_data = []
        if messages_objs:
            for cur_msg_obj in messages_objs:
                cur_msg_data = await _serialize_global_webhook_message_obj(
                    cur_msg_obj=cur_msg_obj)
                paginated_msgs_data.append(cur_msg_data)

        paginated_msgs_details = {
            "paginated_messages": paginated_msgs_data,
            "all_messages_count": all_msgs_count}
        return paginated_msgs_details
    except Exception as error:
        log_text = (f"Getting paginated messages by contacts data [ERROR]:\n"
                    f"error: {error}\n"
                    f"orm_model_class: {GlobalWebhookModel}\n"
                    f"web_account_id: {web_account_id}\n"
                    f"web_account_username: {web_account_username}\n"
                    f"tlt_config_name: {tlt_config_name}\n"
                    f"current_page: {current_page}\n"
                    f"messages_per_page: {messages_per_page}\n")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)

