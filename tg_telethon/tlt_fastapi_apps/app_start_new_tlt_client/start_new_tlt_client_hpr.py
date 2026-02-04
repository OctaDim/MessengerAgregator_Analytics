import asyncio

from fastapi import HTTPException
from starlette import status
from starlette.responses import JSONResponse

from configs.console_colors import CONSOLE_COLORS
from configs.enums import TELEGRAM_ACCOUNT_TYPE
from configs.settings import (
    TELEGRAM_OFFICIAL_APP_API_ID, TELEGRAM_OFFICIAL_APP_API_HASH)
from db_postgres.postgres_models.telethon_configs_model import (
    TelethonConfigModel)
from db_postgres.postgres_queries.qry_cache_new_telethon_config_obj import (
    cache_new_telethon_config_qry)
from tg_telethon.tlt_fastapi_apps.app_start_new_tlt_client.scheme_new_tlt_client import (
    NewTelethonClientData)
from tg_telethon.tlt_fastapi_apps.app_tlt_fastapi_auth.scheme_tlt_auth import (
    TelethonAuthData)
from tg_telethon.tlt_fastapi_apps.app_tlt_fastapi_auth.tlt_funcs_auth import (
    verify_tlt_auth_username_password)
from tg_telethon.tlt_manager.telethon_client_config import (
    TelethonConfig)


async def start_new_tlt_client_helper(
        telethon_auth_data: TelethonAuthData,
        telethon_manager: "TelethonManager",
        new_telethon_client_data: NewTelethonClientData
) -> JSONResponse:
    await verify_tlt_auth_username_password(
        username=telethon_auth_data.username,
        password=telethon_auth_data.password)

    web_account_id = new_telethon_client_data.web_account_id
    web_account_username = new_telethon_client_data.web_account_username
    telegram_phone = new_telethon_client_data.telegram_phone
    bot_token = new_telethon_client_data.telegram_bot_token
    bot_token_id_str = bot_token[:10] if bot_token else None

    if telegram_phone:
        account_type = TELEGRAM_ACCOUNT_TYPE.ACCOUNT
    else:
        account_type = TELEGRAM_ACCOUNT_TYPE.BOT
    account_type_str = account_type.value

    new_tlt_config_data = {
        "web_account_id": web_account_id,
        "web_account_username": web_account_username,
        "tg_account_type": account_type_str,
        "tg_api_id": TELEGRAM_OFFICIAL_APP_API_ID,
        "tg_api_hash": TELEGRAM_OFFICIAL_APP_API_HASH,
        "tg_personal_phone": telegram_phone,
        "tg_bot_token": bot_token_id_str,
        "telethon_is_active": True}

    new_tlt_config_obj: TelethonConfigModel  # just to fix Pycharm annotation warning bug
    new_tlt_config_obj = await cache_new_telethon_config_qry(
        new_telethon_config_data=new_tlt_config_data)
    new_tlt_config_id = new_tlt_config_obj.id

    config_name = await telethon_manager.create_session_name(
        telethon_db_config_id=new_tlt_config_id,
        web_account_id=web_account_id,
        web_account_username=web_account_username,
        telegram_phone=telegram_phone,
        telegram_bot=bot_token_id_str,
        telethon_account_type=account_type_str)

    try:
        new_client_config = TelethonConfig(
            telethon_config_id=new_tlt_config_id,
            web_account_id=web_account_id,
            web_account_username=web_account_username,
            name=config_name,
            account_type=account_type,
            api_id=TELEGRAM_OFFICIAL_APP_API_ID,
            api_hash=TELEGRAM_OFFICIAL_APP_API_HASH,
            session_string=None,
            bot_token=bot_token,
            phone=telegram_phone,
            proxy=None,
            is_active=True)

        new_client = await telethon_manager.run_single_telethon_client(
            telethon_config=new_client_config)

        if not new_client:
            print(f"New Telethon client not authorised and skipped [ERROR]\n"
                  f"new_client: {new_client}\n"
                  f"web_account_id: {web_account_id}\n"
                  f"web_account_username: {web_account_username}\n"
                  f"account_type_str: {account_type_str}\n"
                  f"new_tlt_config_id: {new_tlt_config_id}\n"
                  f"config_name: {config_name}\n"
                  f"telegram_phone: {telegram_phone}\n"
                  f"bot_token_id_str: {bot_token_id_str}\n")

            json_response = JSONResponse(
                content={
                    "message": "Telethon client not authorised and skipped:",
                    "new_client": telethon_auth_data.username,
                    "web_account_id": web_account_id,
                    "web_account_username": web_account_username,
                    "account_type_str": account_type_str,
                    "new_tlt_config_id": new_tlt_config_id,
                    "config_name": config_name,
                    "telegram_phone": telegram_phone,
                    "bot_token_id_str": bot_token_id_str},
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            return json_response
        print(f"{'>' * 55}\n{'>' * 55}\n"
              "New Telethon client created and authorised[OK]:\n"
              f"new_client: {new_client}\n"
              f"new_tlt_config_id: {new_tlt_config_id}\n"
              f"account_type: {account_type}\n"
              f"telegram_phone: {telegram_phone}\n"
              f"bot_token_id_str: {bot_token_id_str}\n"
              f"config_name: {config_name}\n")

        new_client_task = asyncio.create_task(
            coro=new_client.run_until_disconnected(),
            name=config_name,
            context=None)
        telethon_manager.clients[config_name] = new_client
        telethon_manager.running_tasks[config_name] = new_client_task

        json_response = JSONResponse(
            content={"message": "New Telethon client started [OK]",
                     "username": telethon_auth_data.username,
                     "web_account_id": web_account_id,
                     "web_account_username": web_account_username,
                     "account_type_str": account_type_str,
                     "new_tlt_config_id": new_tlt_config_id,
                     "config_name": config_name,
                     "telegram_phone": telegram_phone,
                     "bot_token_id_str": bot_token_id_str},
            status_code=status.HTTP_200_OK)

        blue_clr = CONSOLE_COLORS.BRIGHT_BLUE
        yellow_clr = CONSOLE_COLORS.BRIGHT_YELLOW
        reset_clr = CONSOLE_COLORS.RESET
        print(f"Response.body: {json_response.body}\n"
              f"Response.status_code: {json_response.status_code}\n"
              f"username: {telethon_auth_data.username}\n"
              f"web_account_id: {web_account_id}\n",
              f"web_account_username: {web_account_username}\n",
              f"account_type: {account_type}\n",
              f"new_tlt_config_id: {yellow_clr}{new_tlt_config_id}{reset_clr}\n",
              f"config_name: {blue_clr}{config_name}{reset_clr}\n",
              f"telegram_phone: {telegram_phone}\n",
              f"bot_token_id_str: {bot_token_id_str}\n")
        return json_response
    except Exception as error:
        log_text = (f"Start single Telethon client [ERROR]:\n"
                    f"error: {error}\n"
                    f"username: {telethon_auth_data.username}\n"
                    f"web_account_id: {web_account_id}\n",
                    f"web_account_username: {web_account_username}\n",
                    f"account_type: {account_type}\n",
                    f"new_tlt_config_id: {new_tlt_config_id}\n",
                    f"config_name: {config_name}\n",
                    f"telegram_phone: {telegram_phone}\n",
                    f"bot_token_id_str: {bot_token_id_str}\n")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
