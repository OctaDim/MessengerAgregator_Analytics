from typing import Any, List, Sequence

from fastapi import HTTPException
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db_postgres.postgres_models.webhook_global_model import (
    GlobalWebhookModel)
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_model_rows_flex_query)


async def find_msgs_objs_by_ev_ids_qry(
        ongoing_session: AsyncSession,
        messages_ids: List[int],
) -> Sequence[Row[tuple[Any, ...]]] | None:
    if not messages_ids:
        return None

    filter_fields = {"ev_id": messages_ids}

    messages_objs = await get_model_rows_flex_query(
        orm_model_class=GlobalWebhookModel,
        ongoing_session=ongoing_session,
        selected_fields=None,
        fields_values_filter=filter_fields,
        order_by_fields=GlobalWebhookModel.ev_id,
        # order_by_fields=GlobalWebhookModel.ev_id.desc(),
        return_scalars=True)
    try:
        return messages_objs
    except Exception as error:
        log_text = (f"Finding event messages data by event ids [ERROR]:\n"
                    f"error: {error}\n"
                    f"orm_model_class: {GlobalWebhookModel}\n"
                    f"filter_fields: {filter_fields}\n")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
