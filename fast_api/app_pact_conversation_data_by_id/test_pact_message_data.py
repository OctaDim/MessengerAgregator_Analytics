if __name__ == "__main__":
    from fast_api.app_auth.scheme_auth import AuthDataDiarize
    from fast_api.app_pact_conversation_data_by_id.router_pact_message_data import (
        get_pact_conversation_data)
    from fast_api.app_pact_conversation_data_by_id.scheme_pact_message_data import (
        InConversDataByConverseId)
    import asyncio
    from configs.settings import API_TEST_USERNAME, API_TEST_PASSWORD

    auth_data = AuthDataDiarize(username=API_TEST_USERNAME,
                                password=API_TEST_PASSWORD)

    company_id = "100179"
    conversation_id = "219052460"  # Dima

    pact_api_data = InConversDataByConverseId(
        pact_api_token=None,
        company_id=company_id,
        conversation_id=conversation_id,
        pact_api_timeout=120)

    asyncio.run(
        main=get_pact_conversation_data(
            auth_data=auth_data,
            pact_api_data=pact_api_data),
        debug=True)
