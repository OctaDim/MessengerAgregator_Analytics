if __name__ == "__main__":
    from fast_api.app_auth.scheme_auth import AuthDataDiarize
    from fast_api.app_pact_messages_by_convers.router_messages_by_conversation import (
        get_pact_messages_by_conversation)
    from fast_api.app_pact_messages_by_convers.scheme_messages_by_conversation import (
        InAllMessagesByConversation)
    import asyncio

    auth_data = AuthDataDiarize(username="temp_username",
                                password="temp_password")

    company_id = "100179"
    chat_id = "219052460"  # Dima
    # chat_id = "219052465"  # Thomas

    pact_api_data = InAllMessagesByConversation(
        pact_api_token="0da18787ae6bdbda6329ff5b85720e3a8ea97fe18876cc983f000764218c8c61c098ac5546ac6ea261b384eb53f674ecf25401063f6a6157ba18d45dd6b9c697",
        company_id=company_id,
        conversation_id=chat_id,
        page_number=1,
        items_per_page=100,
        pact_api_timeout=120)

    asyncio.run(
        main=get_pact_messages_by_conversation(
            auth_data=auth_data,
            pact_api_data=pact_api_data),
        debug=True)
