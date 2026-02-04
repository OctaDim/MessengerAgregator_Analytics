from starlette import status
from starlette.responses import JSONResponse

from tg_telethon.tlt_fastapi_apps.app_tlt_fastapi_auth.scheme_tlt_auth import (
    TelethonAuthData)
from tg_telethon.tlt_fastapi_apps.app_tlt_fastapi_auth.tlt_funcs_auth import (
    verify_tlt_auth_username_password)


async def telethon_fastapi_health_check_helper(
        telethon_auth_data: TelethonAuthData,
) -> JSONResponse:
    await verify_tlt_auth_username_password(
        username=telethon_auth_data.username,
        password=telethon_auth_data.password)

    json_response = JSONResponse(
        content={"message": "Telethon FastAPI health check [OK]",
                 "username": telethon_auth_data.username},
        status_code=status.HTTP_200_OK)

    # green_color = CONSOLE_COLORS.BRIGHT_GREEN
    # blue_color = CONSOLE_COLORS.BRIGHT_BLUE
    # reset_color = CONSOLE_COLORS.RESET
    print(f"Response.body: {json_response.body}\n"
          f"Response.status_code: {json_response.status_code}\n"
          f"username: {telethon_auth_data.username}\n")
    return json_response
