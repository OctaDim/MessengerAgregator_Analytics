if __name__ == "__main__":
    from fast_api.app_auth.scheme_auth import AuthData
    from fast_api._pact_fastapi_aps.app_pact_conversation_data_by_id.router_pact_conversation_data import (
        get_pact_conversation_data)
    from fast_api._pact_fastapi_aps.app_pact_conversation_data_by_id.scheme_pact_conversation_data import (
        InConversDataByConversID)
    import asyncio
    from configs.settings import API_USERNAME, API_PASSWORD

    auth_data = AuthData(username=API_USERNAME,
                         password=API_PASSWORD)

    company_id = 100179
    conversation_id = 219052460  # Dima

    pact_api_data = InConversDataByConversID(
        pact_api_token=None,
        company_id=company_id,
        conversation_id=conversation_id,
        pact_api_timeout=120)

    asyncio.run(
        main=get_pact_conversation_data(
            auth_data=auth_data,
            pact_api_data=pact_api_data),
        debug=True)
