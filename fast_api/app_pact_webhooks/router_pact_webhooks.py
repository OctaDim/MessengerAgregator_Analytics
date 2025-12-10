from datetime import datetime

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from configs.settings import (
    WEBHOOKS_OPTIONS, ALCHEMY_OPTIONS, API_USERNAME, API_PASSWORD,
    PACT_API_TOKEN_KEY)
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
from db_postgres.postgres_queries.qry_create_conversation_data import (
    create_conversation_object_qry)
from db_postgres.postgres_queries.qry_find_conversation_obj_by_id import (
    find_convers_obj_by_id_qry)
from db_postgres.postgres_queries_utils.save_new_model_object import (
    save_new_model_data_qry)
from db_postgres.postgres_queries_utils.update_existing_model_object import (
    update_existing_model_objs_qry)
from fast_api.app_auth.scheme_auth import AuthDataAggregator
from fast_api.app_pact_conversation_data_by_id.router_pact_conversation_data import (
    get_pact_conversation_data)
from fast_api.app_pact_conversation_data_by_id.scheme_pact_conversation_data import (
    InConversDataByConversID)
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

    request_dict = await request.json()
    webhook_data = validate_log_pydantic_obj_errors(
        PydanticBaseModel=PactWebhookData,
        request_json=request_dict)

    if WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_OBJ_DATA:
        print(f"WEBHOOK INCOMING DATA:\n"
              f"\tevent_name: {webhook_data.event}\n"
              f"\tevent_type: {webhook_data.type}\n"
              f"\tevent_object: {webhook_data.object}\n"
              f"\tsource: {webhook_data.source}\n"
              f"\toperation: {webhook_data.operation}\n")

    if webhook_data.object:
        event_object = webhook_data.object
        new_pgs_data = {"event": webhook_data.event,
                        "type": webhook_data.type}
        new_pgs_data.update(webhook_data.object)

        pgs_conn = PgsAsyncConnection()
        async with (PgsAsyncSession(engine=pgs_conn.engine,
                                    log_good_ops=log_pgs_good_ops
                                    ) as pgs_session):
            if isinstance(event_object, AuthObject):
                print("####### EVENT: AUTH OBJECT")
                await save_new_model_data_qry(
                    ModelClassORM=WebhookAuthModel,
                    ongoing_session=pgs_session,
                    new_data=new_pgs_data)
            elif isinstance(event_object, ConversationObject):
                print("####### EVENT: CONVERSATION OBJECT")
                company_id = event_object.company_id
                event_convers_id = event_object.id
                existing_convers_obj = await find_convers_obj_by_id_qry(
                    ongoing_session=pgs_session,
                    company_id=company_id,
                    conversation_id=event_convers_id)
                if existing_convers_obj:
                    convers_local_id = existing_convers_obj.local_id
                else:
                    convers_local_id = None

                new_pgs_data.update(
                    {"local_id": convers_local_id})  # If pk is None => creating new object, otherwise updating
                await update_existing_model_objs_qry(
                    ModelClassORM=WebhookConversationModel,
                    ongoing_session=pgs_session,
                    fields_values_filter={
                        "local_id": convers_local_id},
                    update_data=new_pgs_data)
            elif isinstance(event_object, MessageObject):
                print("####### EVENT: MESSAGE OBJECT")
                company_id = event_object.company_id
                event_convers_id = event_object.conversation_id
                existing_convers_obj = await find_convers_obj_by_id_qry(
                    ongoing_session=pgs_session,
                    company_id=company_id,
                    conversation_id=event_convers_id)

                if not existing_convers_obj:  # Conversation was created earlier (before message event) and not webhooked
                    auth_data = AuthDataAggregator(username=API_USERNAME,
                                                   password=API_PASSWORD)
                    pact_api_data = InConversDataByConversID(
                        pact_api_token=PACT_API_TOKEN_KEY,
                        company_id=company_id,
                        conversation_id=event_convers_id,
                        pact_api_timeout=WEBHOOKS_OPTIONS.OUTGOING_EXT_API_REQUEST_TIMEOUT)

                    request_dict = await get_pact_conversation_data(
                        auth_data=auth_data,
                        pact_api_data=pact_api_data)

                    conver_req_data = request_dict["conversation"]
                    conver_req_created_at = conver_req_data["created_at"]
                    dtz_conver_created_at = datetime.fromisoformat(
                        conver_req_created_at.replace('Z', '+00:00'))
                    conver_req_last_updated_at = conver_req_data["last_updated_at"]
                    dtz_conver_last_updated_at = datetime.fromisoformat(
                        conver_req_last_updated_at.replace('Z', '+00:00'))

                    conver_req_data.update({
                        "event": webhook_data.event,  # from conversation event
                        "type": webhook_data.type,  # from conversation type
                        "created_at": dtz_conver_created_at,  # from conversation data request
                        "last_updated_at": dtz_conver_last_updated_at})  # from conversation data request

                    new_convers_obj = await create_conversation_object_qry(
                        ongoing_session=pgs_session,
                        conversation_data=conver_req_data)
                    convers_local_id = new_convers_obj.local_id
                else:
                    convers_local_id = existing_convers_obj.local_id

                new_pgs_data.update({"conversation_local_id": convers_local_id})
                await save_new_model_data_qry(
                    ModelClassORM=WebhookMessageModel,
                    ongoing_session=pgs_session,
                    new_data=new_pgs_data)

                reactions = event_object.reactions
                details = event_object.details
                attachments = event_object.attachments
                if (WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_EXTRA_DATA
                        and any([reactions, details, attachments])):
                    print(f"WEBHOOK EXTRA DATA:\n"
                          f"reactions: {type(reactions)}, {reactions}\n"
                          f"details: {type(details)}, {details}\n"
                          f"attachments: {type(attachments)}, {attachments}\n")
            else:
                print(f"Webhook event object unknown [ERROR]:\n"
                      f"type(event_object): {type(event_object)}\n"
                      f"object: {event_object}\n")

    json_content = {"Message": "Webhook accessed successfully [OK]"}
    json_response = JSONResponse(
        content=json_content,
        status_code=status.HTTP_200_OK)
    return json_response
