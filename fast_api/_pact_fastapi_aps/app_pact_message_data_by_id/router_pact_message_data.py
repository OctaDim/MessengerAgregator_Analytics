import httpx
from fastapi import APIRouter, HTTPException, status

from configs.settings import (
    PACT_WEBHOOKS_OPTIONS, PACT_API_TOKEN_KEY, PACT_API_OPTIONS,
    PACT_API_V2_BASE_URL)
from fast_api.app_auth.funcs_auth import verify_auth_username_password
from fast_api.app_auth.scheme_auth import AuthData
from fast_api._pact_fastapi_aps.app_pact_message_data_by_id.scheme_pact_message_data import (
    InMessageDataByMessageID)

base_url_name = PACT_WEBHOOKS_OPTIONS.WEBHOOKS_API_URL_BASE_NAME
router_pact_get_message_data = APIRouter(prefix=f"/{base_url_name}",
                                         tags=["PACT API ENDPOINTS"])


@router_pact_get_message_data.post(path="/message_data_by_id/",
                                   response_model=None)
async def get_pact_message_data(
        auth_data: AuthData,
        pact_api_data: InMessageDataByMessageID
) -> dict | None:
    await verify_auth_username_password(username=auth_data.username,
                                        password=auth_data.password)
    print(f"{'>' * 75}")
    pact_api_token = pact_api_data.pact_api_token
    pact_api_token = pact_api_token if pact_api_token else PACT_API_TOKEN_KEY

    company_id = pact_api_data.company_id
    conversation_id = pact_api_data.conversation_id
    message_id = pact_api_data.message_id

    page_number = pact_api_data.page_number
    items_per_page = pact_api_data.items_per_page
    pact_api_resp_timeout = pact_api_data.pact_api_timeout

    headers = {"Content-Type": "application/json",
               "X-Private-Api-Token": pact_api_token}

    api_url = f"{PACT_API_V2_BASE_URL}/conversations/{conversation_id}/messages/{message_id}"

    params_data = {"private_api_token": pact_api_token,
                   "company_id": company_id,
                   "page": page_number,
                   "per_page": items_per_page}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=api_url,
                                        headers=headers,
                                        params=params_data,
                                        timeout=pact_api_resp_timeout, )
            response.raise_for_status()
            response_json = response.json()
            if PACT_API_OPTIONS.LOG_MESSAGE_DATA_REQ_RESPONSE:
                print(f"response_json: {response_json}")

            message_data = response_json["message"]
            for cur_param, cur_value in message_data.items():
                print(f"\tcur_param: {cur_param}, "
                      f"type: {type(cur_value)}, "
                      f"cur_value: {cur_value}")
            return dict(response_json)
        except httpx.HTTPStatusError as ext_api_error:
            raise HTTPException(
                status_code=ext_api_error.response.status_code,
                detail=f"External API [ERROR]: error: {ext_api_error}")
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Message Data By Message ID Router [ERROR]:\n"
                       f"error: {error}\n"
                       f"pact_api_data: {pact_api_data}\n")
