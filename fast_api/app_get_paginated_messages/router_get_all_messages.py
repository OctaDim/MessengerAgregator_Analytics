from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from configs.settings import GLOBAL_API_OPTIONS, ALCHEMY_OPTIONS
from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
from db_postgres.postgres_conn.postgres_session import PgsAsyncSession
from db_postgres.postgres_queries.qry_get_paginated_messages import (
    get_paginated_messages_qry)
from fast_api.app_auth.funcs_auth import verify_auth_username_password
from fast_api.app_auth.scheme_auth import AuthData
from fast_api.app_get_paginated_messages.scheme_all_messages import (
    InAllMessagesPagination)
from fast_api.app_web_account.scheme_web_account import (
    InWebAccountData)

base_url_name = GLOBAL_API_OPTIONS.WEBHOOKS_GLOBAL_API_URL_BASE_NAME
router_get_all_messages_list = APIRouter(prefix=f"/{base_url_name}",
                                         tags=["GLOBAL API ENDPOINTS"])


@router_get_all_messages_list.post("/all_messages")
async def get_all_messages_list_router(
        auth_data: AuthData,
        web_account_data: InWebAccountData,
        pagination_data: InAllMessagesPagination,
):
    await verify_auth_username_password(
        username=auth_data.username,
        password=auth_data.password)

    log_pgs_good_ops = ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS

    web_account_id = web_account_data.web_account_id
    web_account_username = web_account_data.web_account_username

    current_page = pagination_data.current_page
    messages_per_page = pagination_data.messages_per_page

    try:
        pgs_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_conn.engine,
                                   log_good_ops=log_pgs_good_ops
                                   ) as pgs_session:
            messages_data = await get_paginated_messages_qry(
                ongoing_session=pgs_session,
                web_account_id=web_account_id,
                web_account_username=web_account_username,
                current_page=current_page,
                messages_per_page=messages_per_page)

        if messages_data:
            paginated_msgs = messages_data["paginated_messages"]
            all_msgs_count = messages_data["all_messages_count"]
            paginated_msgs_count = len(paginated_msgs)
        else:
            paginated_msgs = []
            all_msgs_count = 0
            paginated_msgs_count = 0

        log_txt = (f"Paginated messages received successfully [OK]:\n"
                   # f"paginated_msgs: {paginated_msgs}\n"  # Too long
                   f"paginated_msgs_count: {paginated_msgs_count}\n"
                   f"all_msgs_count: {all_msgs_count}\n")
        print(log_txt)
        json_response = JSONResponse(
            content={"message": log_txt,
                     "username": auth_data.username,
                     "web_account_id": web_account_id,
                     "web_account_username": web_account_username,
                     "current_page": current_page,
                     "messages_per_page": messages_per_page,
                     "paginated_msgs_count": paginated_msgs_count,
                     "all_msgs_count": all_msgs_count,
                     "paginated_msgs": paginated_msgs, },
            status_code=status.HTTP_200_OK)
        return json_response
    except Exception as error:
        error_log = (f"Router Receiving paginated messages [ERROR]: \n"
                     f"error: {error}\n"
                     f"current_page: {current_page}\n"
                     f"messages_per_page: {messages_per_page}\n")
        print(error_log)
        json_response = JSONResponse(
            content=error_log,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return json_response
