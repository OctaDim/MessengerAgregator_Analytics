if __name__ == "__main__":
    from fast_api.app_auth.scheme_auth import AuthDataDiarize
    from fast_api.app_pact_message_data.router_pact_message_data import (
        get_pact_message_data)
    from fast_api.app_pact_message_data.scheme_pact_message_data import (
        InMessageDataByMessageId)
    import asyncio

    auth_data = AuthDataDiarize(username="temp_username",
                                password="temp_password")

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
