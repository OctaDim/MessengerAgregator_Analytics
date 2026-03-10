from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from configs.console_colors import CONSOLE_COLORS
from configs.settings import GLOBAL_API_OPTIONS
from fast_api.app_auth.funcs_auth import verify_auth_username_password
from fast_api.app_auth.scheme_auth import AuthData

base_url_name = GLOBAL_API_OPTIONS.WEBHOOKS_GLOBAL_API_URL_BASE_NAME
rtr_fastapi_health_check = APIRouter(prefix=f"/{base_url_name}",
                                     tags=["GLOBAL API ENDPOINTS"])


@rtr_fastapi_health_check.post("/global_api_health_check")
async def fastapi_health_check_router(
        auth_data: AuthData):
    await verify_auth_username_password(
        username=auth_data.username,
        password=auth_data.password)

    json_response = JSONResponse(
        content={"message": "Global Aggregator API health check [OK]",
                 "username": auth_data.username},
        status_code=status.HTTP_200_OK)

    blue_clr = CONSOLE_COLORS.BRIGHT_BLUE
    yellow_clr = CONSOLE_COLORS.BRIGHT_YELLOW
    green_clr = CONSOLE_COLORS.BRIGHT_GREEN
    reset_clr = CONSOLE_COLORS.RESET
    print(f"Response.body: {json_response.body}\n"
          f"Response.status_code: {green_clr}{json_response.status_code}{reset_clr}\n"
          f"username: {auth_data.username}\n"
          f"message: {yellow_clr}Global Aggregator API health check [OK]{reset_clr}")
    return json_response
