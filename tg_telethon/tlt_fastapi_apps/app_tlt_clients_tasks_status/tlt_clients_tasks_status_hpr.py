from asyncio import Task
from typing import Dict

from starlette import status
from starlette.responses import JSONResponse
from telethon import TelegramClient

from configs.console_colors import CONSOLE_COLORS
from tg_telethon.tlt_fastapi_apps.app_tlt_fastapi_auth.scheme_tlt_auth import (
    TelethonAuthData)
from tg_telethon.tlt_fastapi_apps.app_tlt_fastapi_auth.tlt_funcs_auth import (
    verify_tlt_auth_username_password)


async def telethon_clients_tasks_status_helper(
        telethon_auth_data: TelethonAuthData,
        telethon_clients: Dict[str, TelegramClient],
        asyncio_tasks: dict[str, Task]
) -> JSONResponse:
    await verify_tlt_auth_username_password(
        username=telethon_auth_data.username,
        password=telethon_auth_data.password)

    json_response = JSONResponse(
        content={"message": "Telethon clients tasks status [OK]",
                 "username": telethon_auth_data.username,
                 "clients_running": len(telethon_clients),
                 "tasks": list(asyncio_tasks.keys())},
        status_code=status.HTTP_200_OK)

    green_color = CONSOLE_COLORS.BRIGHT_GREEN
    blue_color = CONSOLE_COLORS.BRIGHT_BLUE
    reset_color = CONSOLE_COLORS.RESET
    print(f"Response.body: {json_response.body}\n"
          f"Response.status_code: {json_response.status_code}\n"
          f"username: {telethon_auth_data.username}\n"
          f"clients_running: {green_color}{len(telethon_clients)}{reset_color}\n"
          f"tasks: {blue_color}{list(asyncio_tasks.keys())}{reset_color}")
    return json_response
