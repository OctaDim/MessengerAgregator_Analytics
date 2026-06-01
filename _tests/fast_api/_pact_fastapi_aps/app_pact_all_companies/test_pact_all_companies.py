if __name__ == "__main__":
    from fast_api.app_auth.scheme_auth import AuthData
    from fast_api._pact_fastapi_aps.app_pact_all_companies.router_pact_all_companies import (
        get_pact_all_companies)
    from fast_api._pact_fastapi_aps.app_pact_all_companies.scheme_pact_all_companies import (
        InPactAllCompanies)
    import asyncio
    from configs.settings import API_USERNAME, API_PASSWORD

    auth_data = AuthData(username=API_USERNAME,
                         password=API_PASSWORD)

    pact_api_data = InPactAllCompanies(
        pact_api_token=None,
        last_req_next_page_token=None,
        items_per_page=100,
        sort_direction="asc",
        pact_api_timeout=120)

    asyncio.run(
        main=get_pact_all_companies(
            auth_data=auth_data,
            pact_api_data=pact_api_data),
        debug=True)
