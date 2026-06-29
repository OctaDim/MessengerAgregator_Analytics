from typing import Dict

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db_postgres.postgres_models.webhook_global_model import (
    GlobalWebhookModel)
from utils_common.serialize_custom_json import get_jsonable_value

PEER_STORAGE_TYPE_TO_MODEL_FIELD = {
    "user": "ev_peer_id_user_id",
    "chat": "ev_peer_id_chat_id",
    "channel": "ev_peer_id_channel_id",
}


async def _serialize_archive_message(cur_msg_obj: GlobalWebhookModel) -> Dict[str, object]:
    ev_date_jsonable = await get_jsonable_value(
        orig_obj_value=cur_msg_obj.ev_date,
        obj_log_name="ev_date",
        log_invalid_json=False)
    ev_edit_date_jsonable = await get_jsonable_value(
        orig_obj_value=cur_msg_obj.ev_edit_date,
        obj_log_name="ev_edit_date",
        log_invalid_json=False)
    ev_delete_date_jsonable = await get_jsonable_value(
        orig_obj_value=cur_msg_obj.ev_delete_date,
        obj_log_name="ev_delete_date",
        log_invalid_json=False)

    sender_title = (
        cur_msg_obj.first_name_cst or
        cur_msg_obj.username_cst or
        cur_msg_obj.tlt_sender_first_name or
        cur_msg_obj.tlt_sender_username or
        "")

    return {
        "archive_id": cur_msg_obj.id,
        "message_id": cur_msg_obj.ev_id,
        "action": cur_msg_obj.action,
        "event_type": cur_msg_obj.event_type,
        "config_name": cur_msg_obj.tlt_config_name,
        "peer_id": (
            cur_msg_obj.ev_peer_id_user_id or
            cur_msg_obj.ev_peer_id_chat_id or
            cur_msg_obj.ev_peer_id_channel_id),
        "peer_storage_type": (
            "user" if cur_msg_obj.ev_peer_id_user_id else
            "chat" if cur_msg_obj.ev_peer_id_chat_id else
            "channel"),
        "text": cur_msg_obj.ev_message_message or "",
        "raw_text": cur_msg_obj.ev_message_raw_text or "",
        "old_text": cur_msg_obj.old_message_message_cst,
        "message_difference": cur_msg_obj.message_difference,
        "chat_title": cur_msg_obj.ev_chat_title,
        "old_chat_title": cur_msg_obj.old_chat_title_cst,
        "date": ev_date_jsonable[1],
        "edit_date": ev_edit_date_jsonable[1],
        "delete_date": ev_delete_date_jsonable[1],
        "out": cur_msg_obj.ev_out,
        "bot": cur_msg_obj.bot_cst,
        "sender_id": cur_msg_obj.ev_sender_id,
        "sender_username": cur_msg_obj.username_cst,
        "sender_first_name": cur_msg_obj.first_name_cst,
        "sender_last_name": cur_msg_obj.last_name_cst,
        "sender_phone": cur_msg_obj.phone_cst,
        "sender_title": sender_title,
        "file_name": cur_msg_obj.file_name_cst,
        "extra_file_name": cur_msg_obj.extra_file_name_cst,
        "s3_bucket": cur_msg_obj.s3_bucket,
        "s3_key": cur_msg_obj.s3_key,
        "s3_uri": cur_msg_obj.s3_uri,
    }


async def get_dialog_messages_archive_qry(
        ongoing_session: AsyncSession,
        web_account_id: str,
        web_account_username: str,
        config_name: str,
        peer_id: int,
        peer_storage_type: str,
        messages_limit: int,
        before_archive_id: int = None,
) -> Dict[str, object]:
    if peer_storage_type not in PEER_STORAGE_TYPE_TO_MODEL_FIELD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported peer_storage_type [ERROR]")

    peer_field_name = PEER_STORAGE_TYPE_TO_MODEL_FIELD[peer_storage_type]
    peer_column = getattr(GlobalWebhookModel, peer_field_name)

    try:
        orm_query = select(GlobalWebhookModel).where(
            GlobalWebhookModel.web_account_id == web_account_id,
            GlobalWebhookModel.web_account_username == web_account_username,
            GlobalWebhookModel.tlt_config_name == config_name,
            peer_column == peer_id)

        if before_archive_id:
            orm_query = orm_query.where(GlobalWebhookModel.id < before_archive_id)

        orm_query = orm_query.order_by(GlobalWebhookModel.id.desc()).limit(
            messages_limit + 1)
        result = await ongoing_session.execute(orm_query)
        message_objs = result.scalars().all()

        has_older = len(message_objs) > messages_limit
        if has_older:
            message_objs = message_objs[:messages_limit]

        archive_messages = []
        for cur_msg_obj in reversed(message_objs):
            archive_messages.append(
                await _serialize_archive_message(cur_msg_obj))

        next_before_archive_id = None
        if archive_messages:
            next_before_archive_id = archive_messages[0]["archive_id"]

        return {
            "archive_messages": archive_messages,
            "has_older": has_older,
            "next_before_archive_id": next_before_archive_id,
        }
    except HTTPException:
        raise
    except Exception as error:
        error_log = (
            "Getting dialog archive messages [ERROR]:\n"
            "error: {error}\n"
            "web_account_id: {web_account_id}\n"
            "web_account_username: {web_account_username}\n"
            "config_name: {config_name}\n"
            "peer_id: {peer_id}\n"
            "peer_storage_type: {peer_storage_type}\n"
        ).format(
            error=error,
            web_account_id=web_account_id,
            web_account_username=web_account_username,
            config_name=config_name,
            peer_id=peer_id,
            peer_storage_type=peer_storage_type,
        )
        print(error_log)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_log)

