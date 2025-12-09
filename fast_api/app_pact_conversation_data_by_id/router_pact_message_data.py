import httpx
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from configs.settings import WEBHOOKS_OPTIONS, PACT_API_TOKEN_KEY
from fast_api.app_auth.funcs_auth import verify_test_username_password
from fast_api.app_auth.scheme_auth import AuthDataDiarize
from fast_api.app_pact_conversation_data_by_id.scheme_pact_message_data import (
    InConversDataByConverseId)

base_url_name = WEBHOOKS_OPTIONS.WEBHOOKS_API_URL_BASE_NAME
router_pact_get_conversation_data = APIRouter(prefix=f"/{base_url_name}",
                                              tags=["PACT API ENDPOINTS"])


@router_pact_get_conversation_data.post(path="/conversation_data_by_id/",
                                        response_model=None)
async def get_pact_conversation_data(
        auth_data: AuthDataDiarize,
        pact_api_data: InConversDataByConverseId
) -> JSONResponse | None:
    verify_test_username_password(username=auth_data.username,
                                  password=auth_data.password)
    print(f"{'>' * 75}")
    pact_api_token = pact_api_data.pact_api_token
    pact_api_token = pact_api_token if pact_api_token else PACT_API_TOKEN_KEY

    company_id = pact_api_data.company_id
    conversation_id = pact_api_data.conversation_id
    pact_api_resp_timeout = pact_api_data.pact_api_timeout

    headers = {"Content-Type": "application/json",
               "X-Private-Api-Token": pact_api_token}

    api_url = f"https://api.pact.im/api/p2/conversations/{conversation_id}"

    params_data = {"private_api_token": pact_api_token,
                   "company_id": company_id}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=api_url,
                                        headers=headers,
                                        params=params_data,
                                        timeout=pact_api_resp_timeout, )
            response.raise_for_status()
            response_json = response.json()
            print(f"response_json: {response_json}")

            message_data = response_json["conversation"]
            for cur_param, cur_value in message_data.items():
                print(f"\tcur_param: {cur_param}, "
                      f"type: {type(cur_value)}, "
                      f"cur_value: {cur_value}")
            return response.json()
        except httpx.HTTPStatusError as ext_api_error:
            raise HTTPException(
                status_code=ext_api_error.response.status_code,
                detail=f"External API [ERROR]: error: {ext_api_error}")
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Conversation Data By Message ID Router [ERROR]:\n"
                       f"error: {error}\n"
                       f"pact_api_data: {pact_api_data}\n")
