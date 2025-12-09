from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db_postgres.postgres_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_model_rows_flex_query)


async def find_conversation_data_by_id(
        ongoing_session: AsyncSession,
        company_id: int,
        conversation_id: int
) -> int | None:
    if not company_id or not conversation_id:
        return None

    filter_fields = {"company_id": company_id,
                     "id": conversation_id}

    conversation_objs = await get_model_rows_flex_query(
        orm_model_class=WebhookConversationModel,
        ongoing_session=ongoing_session,
        selected_fields=["prim_id", "id"],
        fields_values_filter=filter_fields,
        order_by_fields=WebhookConversationModel.prim_id.desc(),
        return_scalars=False)
    try:
        if conversation_objs:
            conversation_id_found = conversation_objs[0].prim_id
            return conversation_id_found
    except Exception as error:
        log_text = (f"Finding or creating conversation data [ERROR]:\n"
                    f"error: {error}\n"
                    f"orm_model_class: {WebhookConversationModel}\n"
                    f"filter_fields: {filter_fields}\n")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
