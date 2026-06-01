import httpx
from fastapi import APIRouter, HTTPException, status

from configs.settings import (
    PACT_WEBHOOKS_OPTIONS, PACT_API_TOKEN_KEY, PACT_API_OPTIONS,
    PACT_API_V1_BASE_URL)
from fast_api._pact_fastapi_aps.app_pact_all_companies.scheme_pact_all_companies import (
    InPactAllCompanies)
from fast_api.app_auth.funcs_auth import verify_auth_username_password
from fast_api.app_auth.scheme_auth import AuthData

base_url_name = PACT_WEBHOOKS_OPTIONS.WEBHOOKS_API_URL_BASE_NAME
router_pact_get_all_companies = APIRouter(prefix=f"/{base_url_name}",
                                          tags=["PACT API ENDPOINTS"])


@router_pact_get_all_companies.post(path="/pct_all_companies/",
                                    response_model=None)
async def get_pact_all_companies(
        auth_data: AuthData,
        pact_api_data: InPactAllCompanies,
) -> dict | None:
    await verify_auth_username_password(username=auth_data.username,
                                        password=auth_data.password)
    print(f"{'>' * 75}")
    pact_api_token = pact_api_data.pact_api_token
    pact_api_token = pact_api_token if pact_api_token else PACT_API_TOKEN_KEY

    last_req_next_page_token = pact_api_data.last_req_next_page_token
    items_per_page = pact_api_data.items_per_page
    sort_direction = pact_api_data.sort_direction
    pact_api_resp_timeout = pact_api_data.last_req_next_page_token

    headers = {"Content-Type": "application/json",
               "X-Private-Api-Token": pact_api_token}

    api_url = f"{PACT_API_V1_BASE_URL}/companies"

    params_data = {
        "private_api_token": pact_api_token,
        "from": last_req_next_page_token,
        "per": items_per_page,
        "sort_direction": sort_direction}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=api_url,
                                        headers=headers,
                                        params=params_data,
                                        timeout=pact_api_resp_timeout, )
            response.raise_for_status()
            response_json = response.json()
            if PACT_API_OPTIONS.LOG_ALL_COMPANIES_REQ_RESPONSE:
                print(f"response_json: {response_json}")

            all_companies = response_json["data"]["companies"]
            next_page_token = response_json["data"].get("next_page", "N/A")

            if PACT_API_OPTIONS.LOG_ALL_COMPANIES_REQ_RESPONSE:
                print(f"next_page_token: {next_page_token}")
                for cur_company in all_companies:
                    print(f"cur_company: {cur_company}")
            return dict(response_json)
        except httpx.HTTPStatusError as ext_api_error:
            raise HTTPException(
                status_code=ext_api_error.response.status_code,
                detail=f"External API [ERROR]: error: {ext_api_error}")
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"All Companies Router [ERROR]:\n"
                       f"error: {error}\n"
                       f"pact_api_data: {pact_api_data}\n")
