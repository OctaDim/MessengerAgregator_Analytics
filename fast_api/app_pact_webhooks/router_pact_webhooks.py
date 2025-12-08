from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from configs.settings import (
    WEBHOOKS_OPTIONS, ALCHEMY_OPTIONS)
from db_postgres.postgres_conn.pgs_connection import (
    PgsAsyncConnection)
from db_postgres.postgres_conn.postgres_session import (
    PgsAsyncSession)
from db_postgres.postgres_models.webhook_auth_model import (
    WebhookAuthModel)
from db_postgres.postgres_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_models.webhook_message_model import (
    WebhookMessageModel)
from db_postgres.postgres_queries_utils.save_new_model_data import (
    save_new_model_data_qry)
from fast_api.app_pact_webhooks.scheme_pact_webhooks import (
    PactWebhookData, MessageObject, AuthObject, ConversationObject)
from utils_common.get_log_request_data import (
    log_all_request_data)
from utils_common.validate_log_pydantic_errors import (
    validate_log_pydantic_obj_errors)

base_url_name = WEBHOOKS_OPTIONS.WEBHOOKS_API_URL_BASE_NAME
router_pact_receive_webhooks = APIRouter(prefix=f"/{base_url_name}",
                                         tags=["PCT ENDPOINTS"])


@router_pact_receive_webhooks.post(path="/webhooks_1/",
                                   response_model=None)
async def receive_pact_webhooks(
        request: Request,
        # webhook_data: PactWebhookData  # validation via func to get errors instead of exception
) -> JSONResponse:
    print(f"{'>' * 75}")
    log_pgs_good_ops = ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS

    if WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_REQ_DATA:
        await log_all_request_data(request=request)

    request_json = await request.json()
    webhook_data = validate_log_pydantic_obj_errors(
        PydanticBaseModel=PactWebhookData,
        request_json=request_json)

    if WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_OBJ_DATA:
        print(f"WEBHOOK INCOMING DATA:\n"
              f"\tevent_name: {webhook_data.event}\n"
              f"\tevent_type: {webhook_data.type}\n"
              f"\tevent_object: {webhook_data.object}\n"
              f"\tsource: {webhook_data.source}\n"
              f"\toperation: {webhook_data.operation}\n")

    if webhook_data.object:
        # TODO: Check, request, save unique conversation id and data mentioned in msg
        # TODO: get certain conversation data and save in conversations
        # TODO: create endpoint getting certain conversation
        event_object = webhook_data.object
        new_pgs_webhook_data = {"event": webhook_data.event,
                                "type": webhook_data.type}
        new_pgs_webhook_data.update(webhook_data.object)

        pgs_conn = PgsAsyncConnection()
        async with (PgsAsyncSession(engine=pgs_conn.engine,
                                    log_good_ops=log_pgs_good_ops
                                    ) as pgs_session):
            if isinstance(event_object, AuthObject):
                await save_new_model_data_qry(
                    ModelClassORM=WebhookAuthModel,
                    ongoing_session=pgs_session,
                    new_data=new_pgs_webhook_data)
            elif isinstance(event_object, ConversationObject):
                await save_new_model_data_qry(
                    ModelClassORM=WebhookConversationModel,
                    ongoing_session=pgs_session,
                    new_data=new_pgs_webhook_data)
            elif isinstance(event_object, MessageObject):
                reactions = event_object.reactions
                details = event_object.details
                attachments = event_object.attachments
                if (WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_EXTRA_DATA
                        and any([reactions, details, attachments])):
                    print(f"WEBHOOK EXTRA DATA:\n"
                          f"reactions: {type(reactions)}, {reactions}\n"
                          f"details: {type(details)}, {details}\n"
                          f"attachments: {type(attachments)}, {attachments}\n")
                await save_new_model_data_qry(
                    ModelClassORM=WebhookMessageModel,
                    ongoing_session=pgs_session,
                    new_data=new_pgs_webhook_data)
            else:
                print(f"Webhook event object unknown [ERROR]:\n"
                      f"type(event_object): {type(event_object)}\n"
                      f"object: {event_object}\n")

    json_content = {"Message": "Webhook accessed successfully [OK]"}
    json_response = JSONResponse(
        content=json_content,
        status_code=status.HTTP_200_OK)
    return json_response
