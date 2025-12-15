# from fastapi import HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status
#
# from db_postgres.postgres_models.message_attachments_model import (
#     MessageAttachmentsModel)
# from db_postgres.postgres_queries_utils.model_object_attrs_update import (
#     update_model_obj_no_commit)
#
#
# async def create_new_conversation_obj_qry(
#         ongoing_session: AsyncSession,
#         attachment_data: dict,
# ) -> MessageAttachmentsModel | None:
#     if not attachment_data:
#         return None
#
#     try:
#         new_attachment_obj = MessageAttachmentsModel()
#         update_model_obj_no_commit(orm_model_object=new_attachment_obj,
#                                    new_update_data=attachment_data)
#         ongoing_session.add(new_attachment_obj)
#         await ongoing_session.flush()
#         return new_attachment_obj
#     except Exception as error:
#         log_text = (f"Creating new attachment data [ERROR]:\n"
#                     f"error: {error}\n"
#                     f"orm_model_class: {MessageAttachmentsModel}\n"
#                     f"attachment_data: {attachment_data}\n")
#         print(log_text)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=log_text)
