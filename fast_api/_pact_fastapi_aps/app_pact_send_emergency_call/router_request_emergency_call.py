import httpx
from fastapi import APIRouter, HTTPException, status

from configs.settings import (
    PACT_WEBHOOKS_OPTIONS, PACT_EMERGENCY_CALL_OPTIONS)
from fast_api.app_auth.funcs_auth import verify_auth_username_password
from fast_api.app_auth.scheme_auth import AuthData
from fast_api._pact_fastapi_aps.app_pact_send_emergency_call.scheme_request_emergency_call import (
    InWarningCallData)

base_url_name = PACT_WEBHOOKS_OPTIONS.WEBHOOKS_API_URL_BASE_NAME
router_request_emergency_call = APIRouter(prefix=f"/{base_url_name}",
                                          tags=["INNER API ENDPOINTS"])


@router_request_emergency_call.post(path="/request_emergency_call/",
                                    response_model=None)
async def request_emergency_call(
        auth_data: AuthData,
        warning_call_data: InWarningCallData,
) -> dict | None:
    await verify_auth_username_password(username=auth_data.username,
                                        password=auth_data.password)
    print(f"{'>' * 75}")
    company_uuid = warning_call_data.company_uuid

    emergency_call_msvc_url = PACT_EMERGENCY_CALL_OPTIONS.EMERGENCY_CALL_URL
    emergency_call_timeout = PACT_EMERGENCY_CALL_OPTIONS.EMERGENCY_CALL_REQUEST_TIMEOUT
    request_data = {"company_uuid": company_uuid, }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url=emergency_call_msvc_url,
                                         data=request_data,
                                         timeout=emergency_call_timeout, )
            response.raise_for_status()
            response_json = response.json()
            response_json.update({"response.status_code": response.status_code})
            if PACT_EMERGENCY_CALL_OPTIONS.LOG_EMERGENCY_CALL_REQ_RESPONSE:
                print(f"response_json: {response_json}")
            return dict(response_json)
        except httpx.HTTPStatusError as ext_api_error:
            raise HTTPException(
                status_code=ext_api_error.response.status_code,
                detail=f"External Emergency Call Microservice [ERROR]:\n"
                       f"error: {ext_api_error}\n"
                       f"company_uuid: {company_uuid}")
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Request Emergency Call Router [ERROR]:\n"
                       f"error: {error}\n"
                       f"company_uuid: {company_uuid}\n")
