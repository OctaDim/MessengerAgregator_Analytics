import asyncio

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
from db_postgres.postgres_queries.qry_get_chat_obj_by_chat_id import find_chat_obj_by_chat_id_qry
from db_postgres.postgres_queries.qry_get_message_obj_by_ev_id import (
    find_msg_obj_by_ev_id_qry)
from db_postgres.postgres_queries_utils.save_new_model_object import (
    save_new_model_object_qry)
from fast_api.app_auth.funcs_auth import verify_prod_username_password
from fast_api.app_global_api_webhooks.router_schemes.scheme_global_api_webhooks import (
    GlobalApiWebhookData)
from utils_common.get_log_request_data import (
    log_all_request_data)
from utils_common.validate_log_pydantic_errors import (
    validate_log_pydantic_obj_errors)
from utils_specific.get_additional_event_data import (
    get_msg_deleted_event_add_data, get_msg_read_event_add_data, get_chat_action_event_add_data)

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
    log_pgs_save_data = GLOBAL_API_WEBHOOKS_OPTIONS.LOG_WEBHOOK_POSTGRES_SAVE_DATA

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
        event_skip_list = GLOBAL_API_WEBHOOKS_OPTIONS.EVENT_TYPES_SKIP_LIST
        if event_skip_list and event_type in event_skip_list:
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
        async with PgsAsyncSession(engine=pgs_conn.engine,
                                   log_good_ops=log_pgs_good_ops
                                   ) as pgs_session:
            event_data_dict = event_data.model_dump()
            if event_type == "NewMessage":
                # isinstance(event_data, NewMessageData):
                custom_action = GLOBAL_API_WEBHOOKS_OPTIONS.NEW_MSG_ACTION_STR
                event_data_dict.update({"action": custom_action})
                new_events_data_list = [event_data_dict]
            elif event_type == "MessageEdited":
                # elif isinstance(event_data, MessageEditedData):
                custom_action = GLOBAL_API_WEBHOOKS_OPTIONS.EDIT_MSG_ACTION_STR
                event_data_dict.update({"action": custom_action})
                new_events_data_list = [event_data_dict]
            elif event_type == "MessageDeleted":
                # elif isinstance(event_data, MessageDeletedData):
                custom_action = GLOBAL_API_WEBHOOKS_OPTIONS.DELETE_MSG_ACTION_STR
                new_events_data_list = []
                for cur_id in event_data.ev_deleted_ids:  # Deleted ids
                    pgs_cur_msg_obj = await find_msg_obj_by_ev_id_qry(
                        ongoing_session=pgs_session,
                        message_ev_id=cur_id)
                    if not pgs_cur_msg_obj:
                        event_data_dict.update({"action": custom_action})
                        new_events_data_list.append(event_data_dict)
                    else:
                        addit_data = await get_msg_deleted_event_add_data(
                            pgs_message_obj=pgs_cur_msg_obj,
                            event_type=event_type)
                        addit_data.update({"action": custom_action})
                        event_data_dict.update(addit_data)
                        new_events_data_list.append(event_data_dict)
            elif event_type == "MessageRead":
                # elif isinstance(event_data, MessageReadData):
                custom_action = GLOBAL_API_WEBHOOKS_OPTIONS.READ_MSG_ACTION_STR
                find_old_msg_attempts = GLOBAL_API_WEBHOOKS_OPTIONS.READ_EVENT_FIND_OLD_MSG_ATTEMPTS
                find_old_msg_delay = GLOBAL_API_WEBHOOKS_OPTIONS.READ_EVENT_FIND_OLD_MSG_DELAY_SEC
                for cur_index in range(find_old_msg_attempts):
                    await asyncio.sleep(cur_index * find_old_msg_delay)
                    pgs_msg_obj = await find_msg_obj_by_ev_id_qry(
                        ongoing_session=pgs_session,
                        message_ev_id=event_data.ev_max_id)
                    if pgs_msg_obj:
                        break
                if not pgs_msg_obj:
                    event_data_dict.update({"action": custom_action})
                    new_events_data_list = [event_data_dict]
                else:
                    addit_data = await get_msg_read_event_add_data(
                        pgs_message_obj=pgs_msg_obj,
                        event_type=event_type)
                    addit_data.update({"action": custom_action})
                    event_data_dict.update(addit_data)
                    new_events_data_list = [event_data_dict]
            elif event_type == "ChatAction":
                custom_action = GLOBAL_API_WEBHOOKS_OPTIONS.CHAT_ACTION_ACTION_STR
                pgs_msg_obj = await find_chat_obj_by_chat_id_qry(
                        ongoing_session=pgs_session,
                        chat_ev_chat_id=event_data.ev_chat_id)
                if not pgs_msg_obj:
                    event_data_dict.update({"action": custom_action})
                    new_events_data_list = [event_data_dict]
                else:
                    addit_data = await get_chat_action_event_add_data(
                        pgs_message_obj=pgs_msg_obj,
                        event_type=event_type)
                    event_data_dict.update({"action": custom_action})
                    event_data_dict.update(addit_data)
                    new_events_data_list = [event_data_dict]
            else:
                new_events_data_list = []

            for cur_event_data in new_events_data_list:
                await save_new_model_object_qry(
                    ModelClassORM=GlobalWebhookModel,
                    ongoing_session=pgs_session,
                    new_data=cur_event_data,
                    skip_invalid_attrs=True,
                    log_new_data=log_pgs_save_data)

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
