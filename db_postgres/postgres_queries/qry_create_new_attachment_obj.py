# from fastapi import HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status
#
# from db_postgres.postgres_models.webhook_conversation_model import (
#     WebhookConversationModel)
# from db_postgres.postgres_queries_utils.model_object_attrs_update import (
#     update_model_obj_no_commit)
#
#
# async def create_new_attachment_obj_qry(
#         ongoing_session: AsyncSession,
#         conversation_data: dict,
# ) -> WebhookConversationModel | None:
#     if not conversation_data:
#         return None
#
#     try:
#         new_conversation_obj = WebhookConversationModel()
#         update_model_obj_no_commit(orm_model_object=new_conversation_obj,
#                                    new_update_data=conversation_data)
#         ongoing_session.add(new_conversation_obj)
#         await ongoing_session.flush()
#         return new_conversation_obj
#     except Exception as error:
#         log_text = (f"Creating new conversation data [ERROR]:\n"
#                     f"error: {error}\n"
#                     f"orm_model_class: {WebhookConversationModel}\n"
#                     f"conversation_data: {conversation_data}\n")
#         print(log_text)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=log_text)
