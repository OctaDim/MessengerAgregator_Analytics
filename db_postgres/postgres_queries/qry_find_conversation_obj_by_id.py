from typing import Any

from fastapi import HTTPException
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db_postgres.postgres_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_model_rows_flex_query)


async def find_conversation_obj_by_id(
        ongoing_session: AsyncSession,
        company_id: int,
        conversation_id: int
) -> Row[tuple[Any, ...]] | None:
    if not company_id or not conversation_id:
        return None

    filter_fields = {"company_id": company_id,
                     "id": conversation_id}

    conversation_objs = await get_model_rows_flex_query(
        orm_model_class=WebhookConversationModel,
        ongoing_session=ongoing_session,
        selected_fields=None,
        fields_values_filter=filter_fields,
        order_by_fields=WebhookConversationModel.local_id.desc(),
        return_scalars=True)
    try:
        if conversation_objs:
            conversation_obj = conversation_objs[0]
            return conversation_obj
    except Exception as error:
        log_text = (f"Finding conversation data [ERROR]:\n"
                    f"error: {error}\n"
                    f"orm_model_class: {WebhookConversationModel}\n"
                    f"filter_fields: {filter_fields}\n")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
