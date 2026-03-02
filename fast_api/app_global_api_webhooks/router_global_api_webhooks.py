from datetime import datetime, timezone

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from configs.settings import (
    ALCHEMY_OPTIONS, GLOBAL_API_WEBHOOKS_OPTIONS, GLOBAL_API_OPTIONS)
from db_postgres.postgres_conn.pgs_connection import (
    PgsAsyncConnection)
from db_postgres.postgres_conn.postgres_session import (
    PgsAsyncSession)
from db_postgres.postgres_models.webhook_global_model import (
    GlobalWebhookModel)
from db_postgres.postgres_queries.qry_get_messages_list_by_ev_ids import (
    find_msgs_objs_by_ev_ids_qry)
from db_postgres.postgres_queries_utils.save_new_model_object import (
    save_new_model_object_qry)
from fast_api.app_auth.funcs_auth import verify_prod_username_password
from fast_api.app_global_api_webhooks.scheme_global_api_webhooks import (
    GlobalApiWebhookData, MessageDeletedData)
from utils_common.get_log_request_data import (
    log_all_request_data)
from utils_common.validate_log_pydantic_errors import (
    validate_log_pydantic_obj_errors)

base_url_name = GLOBAL_API_OPTIONS.WEBHOOKS_GLOBAL_API_URL_BASE_NAME
router_global_api_receive_webhooks = APIRouter(prefix=f"/{base_url_name}",
                                               tags=["GLOBAL API ENDPOINTS"])


@router_global_api_receive_webhooks.post(path="/global_api_webhooks/",
                                         response_model=None)
async def receive_global_api_webhooks(
        request: Request,
        # auth_data: AuthDataAggregator,
        # webhook_data: GlobalApiWebhookData  # validation via func to get errors instead of exception
) -> JSONResponse:
    req_json = await request.json()
    verify_prod_username_password(
        username=req_json["auth_data"]["username"],
        password=req_json["auth_data"]["password"])

    log_pgs_good_ops = ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS

    validation_res = validate_log_pydantic_obj_errors(
        PydanticBaseModel=GlobalApiWebhookData,
        request_json=req_json,
        log_success_validation=GLOBAL_API_OPTIONS.LOG_PYDANTIC_OK_VALIDATION)
    webhook_data = validation_res["validated_obj"]
    if not webhook_data:
        validation_log = validation_res["validation_log"]
        error_log = (f"\nPydantic validation [ERROR]: \n"
                     f"validation_log: {validation_log}\n")
        json_response = JSONResponse(
            content=error_log,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
        return json_response

    try:
        source = webhook_data.source
        operation = webhook_data.operation
        event_data = webhook_data.event_data
        event_type = webhook_data.event_data.event_type

        # DEBUG FUNCTIONALITY ONLY TO SKIP UNNECESSARY WEBHOOKS
        if GLOBAL_API_WEBHOOKS_OPTIONS.DEBUG_EVENT_TYPES_SKIP_LIST:
            if event_type in GLOBAL_API_WEBHOOKS_OPTIONS.DEBUG_EVENT_TYPES_SKIP_LIST:
                log_txt = (f"DEBUG: WEBHOOK SKIPPED [ERROR]: \n"
                           f"event_type: {event_type} \n"
                           f"operation: {operation} \n"
                           f"source: {source}\n")
                print(log_txt)
                json_response = JSONResponse(
                    content=log_txt,
                    status_code=status.HTTP_200_OK)
                return json_response

        print(f"\n{'>' * 75}")
        if GLOBAL_API_WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_REQ_DATA:
            await log_all_request_data(request=request)

        if GLOBAL_API_WEBHOOKS_OPTIONS.LOG_WEBHOOK_INCOMING_OBJ_DATA:
            print(f"\nWEBHOOK INCOMING DATA:\n"
                  f"\tevent_type: {event_type}\n"
                  f"\toperation: {operation}\n"
                  f"\tsource: {source}\n"
                  f"\tevent_data: {event_data}\n")

        pgs_conn = PgsAsyncConnection()
        async with (PgsAsyncSession(engine=pgs_conn.engine,
                                    log_good_ops=log_pgs_good_ops
                                    ) as pgs_session):
            events_data_list = []
            if isinstance(event_data, MessageDeletedData):  # if event_type == "MessageDeleted":
                deleted_msgs_ids = event_data.ev_deleted_ids
                deleted_msgs_objs = await find_msgs_objs_by_ev_ids_qry(
                    ongoing_session=pgs_session,
                    messages_ids=deleted_msgs_ids)

                if not deleted_msgs_objs:
                    events_data_list.append(event_data.model_dump())
                else:
                    del_prfx = GLOBAL_API_WEBHOOKS_OPTIONS.DELETED_MESSAGE_PREFIX
                    for cur_deleted_msg in deleted_msgs_objs:
                        ev_msg = cur_deleted_msg.ev_message_message
                        ev_txt = cur_deleted_msg.ev_message_text
                        ev_raw_txt = cur_deleted_msg.ev_message_raw_text
                        del_msg = f"{del_prfx} {ev_msg}" if ev_msg else f"{del_prfx}"
                        del_txt = f"{del_prfx} {ev_txt}" if ev_txt else f"{del_prfx}"
                        del_raw_txt = f"{del_prfx} {ev_raw_txt}" if ev_raw_txt else f"{del_prfx}"
    
                        additional_data = {
                            "ev_message_message": del_msg,
                            "ev_message_text": del_txt,
                            "ev_message_raw_text": del_raw_txt,
                            "ev_chat_title": cur_deleted_msg.ev_chat_title,
                            "ev_sender_username": cur_deleted_msg.ev_sender_username,
                            "ev_sender_first_name": cur_deleted_msg.ev_sender_first_name,
                            "ev_sender_last_name": cur_deleted_msg.ev_sender_last_name,
                            "ev_sender_bot": cur_deleted_msg.ev_sender_bot,
                            "ev_delete_date": datetime.now(timezone.utc), }
                        new_event_data =event_data.model_dump()
                        new_event_data.update(additional_data)
                        events_data_list.append(new_event_data)
            else:
                events_data_list.append(event_data.model_dump())

            for cur_event_data in events_data_list:
                await save_new_model_object_qry(
                    ModelClassORM=GlobalWebhookModel,
                    ongoing_session=pgs_session,
                    new_data=cur_event_data,
                    skip_invalid_attrs=True,
                    log_new_data=GLOBAL_API_WEBHOOKS_OPTIONS.LOG_WEBHOOK_POSTGRES_SAVE_DATA)

        log_txt = "Webhook saved successfully [OK]"
        print(log_txt)
        json_response = JSONResponse(
            content=log_txt,
            status_code=status.HTTP_200_OK)
        return json_response
    except Exception as error:
        error_log = (f"Global API webhooks router [ERROR]: \n"
                     f"error: {error}\n")
        print(error_log)
        json_response = JSONResponse(
            content=error_log,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
