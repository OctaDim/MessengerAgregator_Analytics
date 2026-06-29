from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from configs.settings import GLOBAL_API_OPTIONS, ALCHEMY_OPTIONS
from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
from db_postgres.postgres_conn.postgres_session import PgsAsyncSession
from db_postgres.postgres_queries.qry_get_dialog_messages_archive import (
    get_dialog_messages_archive_qry)
from fast_api.app_auth.funcs_auth import verify_auth_username_password
from fast_api.app_auth.scheme_auth import AuthData
from fast_api.app_get_dialog_messages_archive.scheme_dialog_messages_archive import (
    InDialogMessagesArchiveData)
from fast_api.app_web_account.scheme_web_account import (
    InWebAccountData)

base_url_name = GLOBAL_API_OPTIONS.WEBHOOKS_GLOBAL_API_URL_BASE_NAME
router_get_dialog_messages_archive = APIRouter(
    prefix=f"/{base_url_name}",
    tags=["GLOBAL API ENDPOINTS"])


@router_get_dialog_messages_archive.post("/dialog_messages_archive")
async def get_dialog_messages_archive_router(
        auth_data: AuthData,
        web_account_data: InWebAccountData,
        dialog_request_data: InDialogMessagesArchiveData,
):
    await verify_auth_username_password(
        username=auth_data.username,
        password=auth_data.password)

    log_pgs_good_ops = ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS

    pgs_conn = PgsAsyncConnection()
    async with PgsAsyncSession(engine=pgs_conn.engine,
                               log_good_ops=log_pgs_good_ops
                               ) as pgs_session:
        archive_data = await get_dialog_messages_archive_qry(
            ongoing_session=pgs_session,
            web_account_id=web_account_data.web_account_id,
            web_account_username=web_account_data.web_account_username,
            config_name=dialog_request_data.config_name,
            peer_id=dialog_request_data.peer_id,
            peer_storage_type=dialog_request_data.peer_storage_type,
            messages_limit=dialog_request_data.messages_limit,
            before_archive_id=dialog_request_data.before_archive_id)

    archive_messages = archive_data["archive_messages"]
    response_content = {
        "message": "Dialog archive messages received [OK]",
        "messenger_type": dialog_request_data.messenger_type,
        "config_name": dialog_request_data.config_name,
        "peer_id": dialog_request_data.peer_id,
        "peer_type": dialog_request_data.peer_type,
        "peer_storage_type": dialog_request_data.peer_storage_type,
        "messages_limit": dialog_request_data.messages_limit,
        "before_archive_id": dialog_request_data.before_archive_id,
        "returned_count": len(archive_messages),
        "has_older": archive_data["has_older"],
        "next_before_archive_id": archive_data["next_before_archive_id"],
        "archive_messages": archive_messages,
    }
    return JSONResponse(
        content=response_content,
        status_code=status.HTTP_200_OK)

