from typing import Any

from fastapi import HTTPException
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db_postgres.postgres_models.webhook_global_model import (
    GlobalWebhookModel)
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_model_rows_flex_query)


async def find_chat_obj_by_chat_id_qry(
        ongoing_session: AsyncSession,
        chat_ev_chat_id: int,
) -> Row[tuple[Any, ...]] | None:
    if not chat_ev_chat_id:
        return None

    filter_fields = {"ev_chat_id": chat_ev_chat_id}

    messages_objs = await get_model_rows_flex_query(
        orm_model_class=GlobalWebhookModel,
        ongoing_session=ongoing_session,
        selected_fields=None,
        fields_values_filter=filter_fields,
        order_by_fields=GlobalWebhookModel.id.desc(),
        return_scalars=True)
    try:
        if messages_objs:
            message_obj = messages_objs[0]
            return message_obj
    except Exception as error:
        log_text = (f"Finding last chat obj by ev_chat_id field [ERROR]:\n"
                    f"error: {error}\n"
                    f"orm_model_class: {GlobalWebhookModel}\n"
                    f"filter_fields: {filter_fields}\n")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
