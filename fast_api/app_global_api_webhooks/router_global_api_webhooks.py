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
from db_postgres.postgres_queries_utils.save_new_model_object import (
    save_new_model_object_qry)
from fast_api.app_auth.funcs_auth import verify_prod_username_password
from fast_api.app_global_api_webhooks.scheme_global_api_webhooks import (
    GlobalApiWebhookData)
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

    webhook_data = validate_log_pydantic_obj_errors(
        PydanticBaseModel=GlobalApiWebhookData,
        request_json=req_json,
        log_success_validation=GLOBAL_API_OPTIONS.LOG_PYDANTIC_OK_VALIDATION)

    if not webhook_data:
        error_log = "Pydantic validation [ERROR]"
        print(error_log)
        json_response = JSONResponse(
            content=error_log,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
        return json_response

    source = webhook_data.source
    operation = webhook_data.operation
    event_data = webhook_data.event_data
    event_type = webhook_data.event_data.event_type

    if hasattr(event_data, "reactions_total_custom"):
        reactions_total_custom = event_data.reactions_total_custom
        print("@@@@@@@@@@@@@@@@@@@@@@ reactions_total_custom", reactions_total_custom)
        print("@@@@@@@@@@@@@@@@@@@@@@ type(reactions_total_custom)", type(reactions_total_custom))
        print()
    if hasattr(event_data, "reactions_total_count_custom"):
        reactions_total_count_custom = event_data.reactions_total_count_custom
        print("@@@@@@@@@@@@@@@@@@@@@@ reactions_total_count_custom", reactions_total_count_custom)
        print("@@@@@@@@@@@@@@@@@@@@@@ type(reactions_total_count_custom)", type(reactions_total_count_custom))
        print()
    if hasattr(event_data, "reactions_emoticon_custom"):
        reactions_emoticon_custom = event_data.reactions_emoticon_custom
        print("@@@@@@@@@@@@@@@@@@@@@@ reactions_emoticon_custom", reactions_emoticon_custom)
        print("@@@@@@@@@@@@@@@@@@@@@@ type(reactions_emoticon_custom)", type(reactions_emoticon_custom))
        print()
    if hasattr(event_data, "reactions_emoticon_count_custom"):
        reactions_emoticon_count_custom = event_data.reactions_emoticon_count_custom
        print("@@@@@@@@@@@@@@@@@@@@@@ reactions_emoticon_count_custom", reactions_emoticon_count_custom)
        print("@@@@@@@@@@@@@@@@@@@@@@ type(reactions_emoticon_count_custom)", type(reactions_emoticon_count_custom))
        print()
    if hasattr(event_data, "reactions_doc_id_custom"):
        reactions_doc_id_custom = event_data.reactions_doc_id_custom
        print("@@@@@@@@@@@@@@@@@@@@@@ reactions_doc_id_custom", reactions_doc_id_custom)
        print("@@@@@@@@@@@@@@@@@@@@@@ type(reactions_doc_id_custom)", type(reactions_doc_id_custom))
        print()
    if hasattr(event_data, "reactions_doc_id_count_custom"):
        reactions_doc_id_count_custom = event_data.reactions_doc_id_count_custom
        print("@@@@@@@@@@@@@@@@@@@@@@ reactions_doc_id_count_custom", reactions_doc_id_count_custom)
        print("@@@@@@@@@@@@@@@@@@@@@@ type(reactions_doc_id_count_custom)", type(reactions_doc_id_count_custom))
        print()

        print("@@@@@@@@@@@@@@@@@@@@@@ webhook_data", webhook_data)
        print("@@@@@@@@@@@@@@@@@@@@@@ type(webhook_data)", type(webhook_data))
        print()

    # DEBUG FUNCTIONALITY ONLY TO SKIP UNNECESSARY WEBHOOKS
    if GLOBAL_API_WEBHOOKS_OPTIONS.DEBUG_SKIP_EVENT_TYPES_LIST:
        if event_type in GLOBAL_API_WEBHOOKS_OPTIONS.DEBUG_SKIP_EVENT_TYPES_LIST:
            log_txt = (f"WEBHOOK SKIPPED [OK]: event_type: {event_type}\n"
                       f"operation: {operation}, source: {source}\n")
            print(log_txt)
            json_response = JSONResponse(
                content={"Message": log_txt},
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
        await save_new_model_object_qry(
            ModelClassORM=GlobalWebhookModel,
            ongoing_session=pgs_session,
            new_data=event_data.model_dump(),
            skip_invalid_attrs=True,
            log_new_data=GLOBAL_API_WEBHOOKS_OPTIONS.LOG_WEBHOOK_POSTGRES_SAVE_DATA)

    log_txt = "Webhook saved successfully [OK]"
    print(log_txt)
    json_response = JSONResponse(
        content=log_txt,
        status_code=status.HTTP_200_OK)
    return json_response
