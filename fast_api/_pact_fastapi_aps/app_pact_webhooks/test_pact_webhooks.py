if __name__ == "__main__":
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from utils_common.validate_log_pydantic_errors import (
        validate_log_pydantic_obj_errors)
    from fast_api._pact_fastapi_aps.app_pact_webhooks.router_pact_webhooks import (
        router_pact_receive_webhooks)
    from fast_api._pact_fastapi_aps.app_pact_webhooks.scheme_pact_webhooks import (
        PactWebhookData)

    fastapi_app = FastAPI()
    fastapi_app.include_router(router_pact_receive_webhooks)


    with TestClient(app=fastapi_app) as fastapi_client:
        test_webhook_data = {"event": "some string"}
        test_webhook_data = {"source": "pact.im", "operation": "test"}
        # test_webhook_data = {"pydantic not included": "some value"}
        # test_webhook_data = {}
        # test_webhook_data = None

        model_validate_result = PactWebhookData.model_validate(test_webhook_data)
        print("model_validate_result: ", model_validate_result)

        validate_log_pydantic_obj_errors(
            PydanticBaseModel=PactWebhookData,
            request_json=test_webhook_data)

        test_response = fastapi_client.post(
            url="http://176.124.136.22:8010/agregator_api/webhooks_1/",
            json=test_webhook_data)

        print("test_response: ", test_response)
