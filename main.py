# from sqladmin import Admin
# from starlette.applications import Starlette
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware

from admin_panel.admin_views.__temp.admin_auth_role_backend import (
    AdminAuthRoleAuthBackend)
from admin_panel.admin_views.admin_chats_subjects import (
    ChatSubjectsAdmin)
from admin_panel.admin_views.admin_conversations import (
    ConversationsAdmin)
from admin_panel.admin_views.admin_keywords_minus import (
    MinusKeywordsAdmin)
from admin_panel.admin_views.admin_keywords_plus import (
    PlusKeywordsAdmin)
from admin_panel.admin_views.admin_messages import MessagesAdmin
from configs.labels_messages import LABELS
from configs.settings import (
    API_HOST, API_PORT, FASTAPI_OPTIONS, FASTAPI_SESSION_KEY,
    SQLADMIN_OPTIONS)
from db_postgres.postgres_conn.pgs_connection import (
    close_all_async_pgs_connections, close_all_sync_pgs_connections,
    PgsAsyncConnection)
from db_postgres.postgres_init.db_create_sqladmin_users import (
    create_default_sqladmin_users)
from db_postgres.postgres_init.db_tables_initialization import (
    sync_initialize_db_tables)
from fast_api.app_pact_all_conversations.router_pact_all_conversations import (
    router_pact_get_all_conversations)
from fast_api.app_pact_message_data_by_id.router_pact_message_data import (
    router_pact_get_message_data)
from fast_api.app_pact_messages_by_conversation.router_messages_by_conversation import (
    router_pact_get_messages_by_convers)
from fast_api.app_pact_webhooks.router_pact_webhooks import (
    router_pact_receive_webhooks)
from fast_api.app_root_url.router_main import router_root_url
from fast_api.app_test_endpoint.router_test_endpoint import (
    router_develop_test_endpoint)

routers_list = [
    router_root_url,
    router_pact_get_all_conversations,
    router_pact_get_messages_by_convers,
    router_pact_get_message_data,
    router_pact_receive_webhooks,

    # Test end-point (debug time)
    router_develop_test_endpoint,
]

admin_panel_views = [
    ConversationsAdmin,
    MessagesAdmin,
    ChatSubjectsAdmin,
    PlusKeywordsAdmin,
    MinusKeywordsAdmin,
]


def initialize_postgres_db_tables():
    sync_initialize_db_tables()
    pass


def run_redis():
    # TODO: Check Redis is available and start Redis if not
    print("TODO: Check Redis is available and start Redis if not")
    pass


def run_postgres():
    # TODO: Check Postgres is available and start Postgres if not
    print("TODO: Check Postgres is available and start Postgres if not")
    pass


async def lifespan_on_startup():
    print(">>>>>>> FastAPI Lifespan (startup):")
    # run_redis()
    run_postgres()
    await create_default_sqladmin_users()  # Creating default sqladmin users
    # await init_and_start_bert_model()  # Initializing Bert model


async def lifespan_on_shutdown():
    print(">>>>>>> FastAPI Lifespan (shutdown):")
    await close_all_async_pgs_connections()
    close_all_sync_pgs_connections()


@asynccontextmanager
async def fast_api_lifespan(app: FastAPI) -> AsyncGenerator:
    await lifespan_on_startup()
    yield  # FastAPI lifespan yield  (Execution fastapi application)
    await lifespan_on_shutdown()


def setup_admin_panel(
        application: FastAPI | Starlette,
        fastapi_session_key: str
) -> Admin:
    authentication_backend = AdminAuthRoleAuthBackend(
        secret_key=fastapi_session_key)
    admin = Admin(
        app=application,
        engine=PgsAsyncConnection().engine,
        authentication_backend=authentication_backend,
        session_maker=None,
        base_url=SQLADMIN_OPTIONS.SQLADMIN_PANEL_BASE_URL,
        title=LABELS.ADMIN_PANEL_TITLE,
        logo_url=None,
        favicon_url=None,
        middlewares=None,
        debug=False,
        templates_dir=SQLADMIN_OPTIONS.SQLADMIN_CUSTOM_TEMPLATES_DIR, )  # Origin SQLAdmin value = "templates"
    for cur_admin_view in admin_panel_views:
        admin.add_view(cur_admin_view)
    return admin


def create_fastapi_application() -> SessionMiddleware:
    fastapi_app = FastAPI(
        lifespan=fast_api_lifespan,
        docs_url=None,
        redoc_url=None, )

    for cur_router in routers_list:
        fastapi_app.include_router(router=cur_router, )

    setup_admin_panel(application=fastapi_app,
                      fastapi_session_key=FASTAPI_SESSION_KEY)

    fastapi_app_with_middleware = SessionMiddleware(
        app=fastapi_app,
        secret_key=FASTAPI_SESSION_KEY,
        session_cookie="admin_session",
        max_age=600,
        path="/",
        same_site="lax",  # "lax", "strict" or "none"
        https_only=False,
        domain=None)

    # return fastapi_app
    return fastapi_app_with_middleware


def run_uvicorn_fastapi_server():
    uvicorn.run(app=create_fastapi_application(),
                # app="main:create_fastapi_app",  # literal func call is necessary if server reload=True when code changing
                host=API_HOST,
                port=API_PORT,
                # reload=True,
                # factory=True,
                log_level=FASTAPI_OPTIONS.LOG_LEVEL,
                use_colors=FASTAPI_OPTIONS.USE_COLORS, )
    print("Uvicorn and FastAPI server started [OK]")


if __name__ == "__main__":
    initialize_postgres_db_tables()
    run_uvicorn_fastapi_server()
