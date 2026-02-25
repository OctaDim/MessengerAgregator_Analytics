from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from configs.settings import (
    ALCHEMY_OPTIONS, GLOBAL_API_WEBHOOKS_OPTIONS, GLOBAL_API_OPTIONS)
from db_postgres.postgres_conn.pgs_connection import (
    PgsAsyncConnection)
from db_postgres.postgres_conn.postgres_session import (
    PgsAsyncSession)
from db_postgres.postgres_models.webhook_global_api_model import (
    GlobalWebhookMsgModel)
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

    source = webhook_data.source
    operation = webhook_data.operation
    event_data = webhook_data.event_data
    event_type = event_data.event_type

    if hasattr(event_data, "ev_views"):
        ev_views = event_data.ev_views
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ev_views", ev_views)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ type(ev_views)", type(ev_views))
        print()
    if hasattr(event_data, "ev_reactions"):
        ev_reactions = event_data.ev_reactions
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ev_reactions", ev_reactions)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ type(ev_reactions)", type(ev_reactions))
        print()
    if hasattr(event_data, "ev_replies"):
        ev_replies = event_data.ev_replies
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ev_replies", ev_replies)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ type(ev_replies)", type(ev_replies))
        print()
    if hasattr(event_data, "ev_forwards"):
        ev_forwards = event_data.ev_forwards
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ev_forwards", ev_forwards)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ type(ev_forwards)", type(ev_forwards))
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
            ModelClassORM=GlobalWebhookMsgModel,
            ongoing_session=pgs_session,
            new_data=event_data.model_dump(),
            skip_invalid_attrs=True,
            log_new_data=GLOBAL_API_WEBHOOKS_OPTIONS.LOG_WEBHOOK_NEW_MSG_DATA)

    json_content = {"Message": "Webhook saved successfully [OK]"}
    json_response = JSONResponse(
        content=json_content,
        status_code=status.HTTP_200_OK)
    return json_response
