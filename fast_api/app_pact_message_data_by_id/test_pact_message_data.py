if __name__ == "__main__":
    from fast_api.app_auth.scheme_auth import AuthDataDiarize
    from fast_api.app_pact_message_data_by_id.router_pact_message_data import (
        get_pact_message_data)
    from fast_api.app_pact_message_data_by_id.scheme_pact_message_data import (
        InMessageDataByMessageId)
    import asyncio
    from configs.settings import API_TEST_USERNAME, API_TEST_PASSWORD

    auth_data = AuthDataDiarize(username=API_TEST_USERNAME,
                                password=API_TEST_PASSWORD)

    company_id = "100179"
    chat_id = "219052460"  # Dima
    # chat_id = "219052465"  # Thomas
    message_id = "1410098920"  # Dima

    pact_api_data = InMessageDataByMessageId(
        pact_api_token=None,
        company_id=company_id,
        conversation_id=chat_id,
        message_id=message_id,
        page_number=1,
        items_per_page=100,
        pact_api_timeout=120)

    asyncio.run(
        main=get_pact_message_data(
            auth_data=auth_data,
            pact_api_data=pact_api_data),
        debug=True)
