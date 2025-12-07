if __name__ == "__main__":
    from fast_api.app_auth.scheme_auth import AuthDataDiarize
    from fast_api.app_pact_all_conversations.router_pact_all_conversations import (
        get_pact_all_conversations)
    from fast_api.app_pact_all_conversations.scheme_pact_all_conversations import (
        InPactAllConversations)
    import asyncio
    from configs.settings import API_TEST_USERNAME, API_TEST_PASSWORD

    auth_data = AuthDataDiarize(username=API_TEST_USERNAME,
                                password=API_TEST_PASSWORD)

    company_id = "100179"

    pact_api_data = InPactAllConversations(
        pact_api_token=None,
        company_id=company_id,
        page_number=1,
        items_per_page=100,
        pact_api_timeout=120)

    asyncio.run(
        main=get_pact_all_conversations(
            auth_data=auth_data,
            pact_api_data=pact_api_data),
        debug=True)
