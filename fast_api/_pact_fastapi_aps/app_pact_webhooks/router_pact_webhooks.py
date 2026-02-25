import os.path
from datetime import datetime

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from configs.filters import SQLADMIN_FILTERS
from configs.settings import (
    PACT_WEBHOOKS_OPTIONS, ALCHEMY_OPTIONS, API_USERNAME, API_PASSWORD,
    PACT_API_TOKEN_KEY, PACT_API_OPTIONS, PACT_SQLADMIN_OPTIONS)
from db_postgres.postgres_conn.pgs_connection import (
    PgsAsyncConnection)
from db_postgres.postgres_conn.postgres_session import (
    PgsAsyncSession)
from db_postgres.postgres_models._pact_pgs_models.message_attachments_model import (
    MessageAttachmentsModel)
from db_postgres.postgres_models._pact_pgs_models.webhook_auth_model import (
    WebhookAuthModel)
from db_postgres.postgres_models._pact_pgs_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_models._pact_pgs_models.webhook_message_model import (
    WebhookMessageModel)
from db_postgres.postgres_queries._pact_pgs_queries.qry_find_conversation_obj_by_id import (
    find_convers_obj_by_id_qry)
from db_postgres.postgres_queries._pact_pgs_queries.qry_get_plus_minus_keywords_list import (
    get_plus_keywords_list_qry)
from db_postgres.postgres_queries_utils.create_cache_new_model_object import (
    create_cache_new_model_obj_qry)
from db_postgres.postgres_queries_utils.update_existing_model_objects import (
    update_existing_model_objs_qry)
from fast_api.app_auth.scheme_auth import AuthDataAggregator
from fast_api._pact_fastapi_aps.app_pact_all_companies.router_pact_all_companies import get_pact_all_companies
from fast_api._pact_fastapi_aps.app_pact_all_companies.scheme_pact_all_companies import InPactAllCompanies
from fast_api._pact_fastapi_aps.app_pact_conversation_data_by_id.router_pact_conversation_data import (
    get_pact_conversation_data)
from fast_api._pact_fastapi_aps.app_pact_conversation_data_by_id.scheme_pact_conversation_data import (
    InConversDataByConversID)
from fast_api._pact_fastapi_aps.app_pact_webhooks.scheme_pact_webhooks import (
    PactWebhookData, MessageObject, AuthObject, ConversationObject)
from fast_api._pact_fastapi_aps.app_pact_send_emergency_call.router_request_emergency_call import (
    request_emergency_call)
from fast_api._pact_fastapi_aps.app_pact_send_emergency_call.scheme_request_emergency_call import (
    InWarningCallData)
from utils_common.get_log_request_data import (
    log_all_request_data)
from utils_common.validate_log_pydantic_errors import (
    validate_log_pydantic_obj_errors)

base_url_name = PACT_WEBHOOKS_OPTIONS.WEBHOOKS_API_URL_BASE_NAME
router_pact_receive_webhooks = APIRouter(prefix=f"/{base_url_name}",
                                         tags=["PACT API ENDPOINTS"])


@router_pact_receive_webhooks.post(path="/webhooks_1/",
                                   response_model=None)
async def receive_pact_webhooks(
        request: Request,
        # webhook_data: PactWebhookData  # validation via func to get errors instead of exception
) -> JSONResponse:
    log_pgs_good_ops = ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS

    # DEBUG FUNCTIONALITY ONLY TO SKIP UNNECESSARY WEBHOOKS
    if PACT_WEBHOOKS_OPTIONS.DEBUG_SKIP_COMPANY_IDS_LIST:
        pact_resp_json = await request.json()
        event_name = pact_resp_json.get("type")
        event_type = pact_resp_json.get("event")
        skip_list = ["new", "ack"]
        old_version_webhook_flag = any([
            event_name == "group_message",
            event_name == "message" and event_type in skip_list, ])

        if old_version_webhook_flag:
            log_txt = (f"WEBHOOK SKIPPED [OK]: "
                       f"type: {event_name}, event: {event_type}, "
                       f"old_version_webhook_flag: {old_version_webhook_flag}")
            print(log_txt)
            json_response = JSONResponse(
                content={"Message": log_txt},
                status_code=status.HTTP_200_OK)
            return json_response
        webhook_data = validate_log_pydantic_obj_errors(
            PydanticBaseModel=PactWebhookData,
            request_json=pact_resp_json,
            log_success_validation=PACT_API_OPTIONS.LOG_PYDANTIC_OK_VALIDATION)
        if webhook_data.object:
            event_obj = webhook_data.object
            if isinstance(event_obj, (MessageObject, ConversationObject)):
                company_id = event_obj.company_id
                skip_company_id_flag = (
                        company_id in PACT_WEBHOOKS_OPTIONS.DEBUG_SKIP_COMPANY_IDS_LIST)

                if skip_company_id_flag:
                    log_txt = (f"WEBHOOK SKIPPED [OK]: "
                               f"type: {event_name}, event: {event_type}, "
                               f"company_id: {company_id}, "
                               f"skip_company_id_flag: {skip_company_id_flag}")
                    print(log_txt)
                    json_response = JSONResponse(
                        content={"Message": log_txt},
                        status_code=status.HTTP_200_OK)
                    return json_response

    print(f"\n{'>' * 75}")
    if PACT_WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_REQ_DATA:
        await log_all_request_data(request=request)

    pact_response_json = await request.json()
    webhook_data = validate_log_pydantic_obj_errors(
        PydanticBaseModel=PactWebhookData,
        request_json=pact_response_json,
        log_success_validation=PACT_API_OPTIONS.LOG_PYDANTIC_OK_VALIDATION)

    if PACT_WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_OBJ_DATA:
        print(f"\nWEBHOOK INCOMING DATA:\n"
              f"\tevent_name: {webhook_data.event}\n"
              f"\tevent_name: {webhook_data.type}\n"
              f"\tevent_object: {webhook_data.object}\n"
              f"\tsource: {webhook_data.source}\n"
              f"\toperation: {webhook_data.operation}\n")

    if webhook_data.object:
        event_object = webhook_data.object
        new_event_data = {"event": webhook_data.event,
                          "type": webhook_data.type}
        new_event_data.update(webhook_data.object)

        pgs_conn = PgsAsyncConnection()
        async with (PgsAsyncSession(engine=pgs_conn.engine,
                                    log_good_ops=log_pgs_good_ops
                                    ) as pgs_session):
            if isinstance(event_object, AuthObject):
                print("\n####### EVENT: AUTH OBJECT")
                new_auth_obj = await create_cache_new_model_obj_qry(
                    ModelClassORM=WebhookAuthModel,
                    ongoing_session=pgs_session,
                    new_data=new_event_data,
                    log_new_data=PACT_WEBHOOKS_OPTIONS.LOG_WEBHOOK_NEW_AUTH_DATA)
            elif isinstance(event_object, ConversationObject):
                print("\n####### EVENT: CONVERSATION OBJECT")
                event_convers_id = event_object.id

                # ##### Option 1. Update only last by id conversation object
                # company_id = event_object.company_id
                # existing_convers_obj = await find_convers_obj_by_id_qry(
                #     ongoing_session=pgs_session,
                #     company_id=company_id,
                #     conversation_id=event_convers_id)
                # if existing_convers_obj:
                #     convers_local_id = existing_convers_obj.local_id
                # else:
                #     convers_local_id = None
                # new_event_data.update(
                #     {"local_id": convers_local_id})  # If pk is None => creating new object, otherwise updating

                # ##### Option 2. Update all conversations with id = event_convers_id
                await update_existing_model_objs_qry(
                    ModelClassORM=WebhookConversationModel,
                    ongoing_session=pgs_session,
                    fields_values_filter={
                        # "local_id": convers_local_id,  # Option 1. To update only last conversation object
                        "id": event_convers_id,  # Option 2. Update all conversations with id = event_convers_id
                    },
                    update_data=new_event_data)
            elif isinstance(event_object, MessageObject):
                print("\n####### EVENT: MESSAGE OBJECT")
                pact_api_timeout = PACT_WEBHOOKS_OPTIONS.OUTGOING_EXT_API_REQ_TIMEOUT
                message = event_object.message
                plus_keywords_list = await get_plus_keywords_list_qry(
                    ongoing_sync_session=pgs_session)

                if PACT_WEBHOOKS_OPTIONS.MAKE_EMERGENCY_CALL:
                    for cur_plus_keyword in plus_keywords_list:
                        if cur_plus_keyword in message.lower():
                            print(f"\n\n####### 15 MINUTES CALL (START)\n"
                                  f"cur_plus_keyword: {cur_plus_keyword}\n"
                                  f"message: {message.lower()}\n\n")

                            try:
                                auth_data = AuthDataAggregator(
                                    username=API_USERNAME,
                                    password=API_PASSWORD)
                                pact_data = InPactAllCompanies(
                                    pact_api_token=PACT_API_TOKEN_KEY,
                                    pact_api_timeout=pact_api_timeout, )
                                companies_dict = await get_pact_all_companies(
                                    auth_data=auth_data,
                                    pact_api_data=pact_data)
                                companies_list = companies_dict["data"]["companies"]
                                for cur_company in companies_list:
                                    external_id = cur_company["external_id"]
                                    if event_object.company_id == external_id:
                                        ext_co_uuid = cur_company["external_uuid"]

                                warning_call_data = InWarningCallData(
                                    company_uuid=ext_co_uuid)
                                call_response_dict = await request_emergency_call(
                                    auth_data=auth_data,
                                    warning_call_data=warning_call_data)
                                print(f"\n\n####### 15 MINUTES CALL (END)\n"
                                      f"call_response_dict: {call_response_dict}\n\n")
                            except Exception as emergency_call_error:
                                print(f"\n\n####### 15 MINUTES CALL (ERROR)\n"
                                      f"emergency_call_error: {emergency_call_error}\n\n")

                company_id = event_object.company_id
                event_convers_id = event_object.conversation_id
                existing_convers_obj = await find_convers_obj_by_id_qry(
                    ongoing_session=pgs_session,
                    company_id=company_id,
                    conversation_id=event_convers_id)

                if not existing_convers_obj:  # Conversation was created earlier (before message event) and not webhooked
                    req_auth_data = AuthDataAggregator(username=API_USERNAME,
                                                       password=API_PASSWORD)
                    req_pact_api_data = InConversDataByConversID(
                        pact_api_token=PACT_API_TOKEN_KEY,
                        company_id=company_id,
                        conversation_id=event_convers_id,
                        pact_api_timeout=pact_api_timeout)

                    pact_response_json = await get_pact_conversation_data(
                        auth_data=req_auth_data,
                        pact_api_data=req_pact_api_data)

                    conver_req_data = pact_response_json["conversation"]
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

                    new_convers_obj = await create_cache_new_model_obj_qry(
                        ModelClassORM=WebhookConversationModel,
                        ongoing_session=pgs_session,
                        new_data=conver_req_data,
                        log_new_data=PACT_WEBHOOKS_OPTIONS.LOG_NEW_CONVERSATION_DATA)
                    convers_local_id = new_convers_obj.local_id
                    convers_provider = new_convers_obj.provider  # from conversation model
                    sender_name = new_convers_obj.sender_name  # from conversation model
                else:
                    convers_local_id = existing_convers_obj.local_id
                    convers_provider = existing_convers_obj.provider  # from conversation model
                    sender_name = existing_convers_obj.sender_name  # from conversation model

                reactions = event_object.reactions
                details = event_object.details
                attachments = event_object.attachments
                if PACT_WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_EXTRA_DATA:
                    # if (PACT_WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_EXTRA_DATA
                    #         and any([reactions, details, attachments])):
                    print(f"WEBHOOK EXTRA DATA:\n"
                          f"reactions: {type(reactions)}, {reactions}\n"
                          f"details: {type(details)}, {details}\n"
                          f"attachments: {type(attachments)}, {attachments}\n")

                if attachments:
                    file_name = attachments[0].get("file_name")
                    mime_type = attachments[0].get("mime_type")
                    push_to_talk = attachments[0].get("push_to_talk")
                    attached_file_data = {
                        "file_name": file_name,
                        "mime_type": mime_type,
                        "push_to_talk": push_to_talk,
                        "attachment_url": attachments[0].get("attachment_url"), }
                    new_event_data.update(attached_file_data)

                    _, file_ext = os.path.split(file_name)
                    file_ext = file_ext.replace(".", "")
                    file_aspect_ratio = attachments[0].get("aspect_ratio")
                    f_data = attachments[0].get("data")
                    f_width = f_data.get("width", None) if f_data else None
                    f_height = f_data.get("height", None) if f_data else None

                    is_emoji_type_flag = any([
                        file_ext in SQLADMIN_FILTERS.EMOJI_FILTER_EXTENSIONS,
                        mime_type in SQLADMIN_FILTERS.EMOJI_FILTER_MIME_TYPES, ])

                    is_emoji_size_flag = all([
                        file_aspect_ratio and file_aspect_ratio == 1,
                        f_width and f_width <= PACT_SQLADMIN_OPTIONS.EMOJI_MAX_WIDTH,
                        f_height and f_height <= PACT_SQLADMIN_OPTIONS.EMOJI_MAX_HEIGHT, ])

                    has_emoji_flag = any([
                        is_emoji_type_flag, is_emoji_size_flag, ])

                    if has_emoji_flag:
                        print(f"\n\n{'#' * 50}\n{'#' * 50}\n"
                              f"HAS EMOJI FLAG (START)\n"
                              f"{'#' * 50}\n{'#' * 50}\n\n")

                data_from_convers = {
                    "conversation_local_id": convers_local_id,
                    "provider": convers_provider,
                    "sender_name": sender_name}
                new_event_data.update(data_from_convers)

                new_message_obj = await create_cache_new_model_obj_qry(
                    ModelClassORM=WebhookMessageModel,
                    ongoing_session=pgs_session,
                    new_data=new_event_data,
                    log_new_data=PACT_WEBHOOKS_OPTIONS.LOG_NEW_MESSAGE_DATA)
                message_local_id = new_message_obj.local_id

                if attachments:
                    new_attachment_data = {
                        "event": webhook_data.event,  # from conversation event
                        "type": webhook_data.type,  # from conversation type
                        "message_local_id": message_local_id}

                    new_attachment_data.update(attachments[0])  # PACT Support: one message per attachment
                    await create_cache_new_model_obj_qry(
                        ModelClassORM=MessageAttachmentsModel,
                        ongoing_session=pgs_session,
                        new_data=new_attachment_data,
                        log_new_data=PACT_WEBHOOKS_OPTIONS.LOG_NEW_ATTACHMENT_DATA)

            else:
                print(f"UNKNOWN WEBHOOK EVENT OBJECT [ERROR]:\n"
                      f"type(event_object): {type(event_object)}\n"
                      f"object: {event_object}\n")

    json_content = {"Message": "Webhook accessed successfully [OK]"}
    json_response = JSONResponse(
        content=json_content,
        status_code=status.HTTP_200_OK)
    return json_response
