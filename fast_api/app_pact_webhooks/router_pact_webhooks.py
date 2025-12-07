from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from configs.settings import WEBHOOKS_OPTIONS
from fast_api.app_pact_webhooks.func_validate_webhook import (
    validate_log_pydantic_errors)
from fast_api.app_pact_webhooks.scheme_pact_webhooks import (
    PactWebhookData, MessageObj, AuthObj, ConversationObj)
from utils_common.get_log_request_data import log_all_request_data

base_url_name = WEBHOOKS_OPTIONS.WEBHOOKS_API_URL_BASE_NAME
router_pact_receive_webhooks = APIRouter(prefix=f"/{base_url_name}",
                                         tags=["PCT ENDPOINTS"])


@router_pact_receive_webhooks.post(path="/webhooks_1/",
                                   response_model=None)
async def receive_pact_webhooks(
        request: Request,
        webhook_data: PactWebhookData
) -> JSONResponse:
    print(f"{'>' * 75}")
    await log_all_request_data(request=request)

    request_json = await request.json()
    print(f"request_json: {request_json}")
    validate_log_pydantic_errors(
        PydanticBaseModel=PactWebhookData,
        request_json=request_json)

    event_name = webhook_data.event
    event_type = webhook_data.type
    event_object = webhook_data.object
    source = webhook_data.source
    operation = webhook_data.operation
    print(f"webhook_data: \n"
          f"event_name: {event_name or 'None'}\n"
          f"event_type: {event_type or 'None'}\n"
          f"event_object: {event_object or 'None'}\n"
          f"source: {source or 'None'}\n"
          f"operation: {operation or 'None'}\n")

    if event_object:
        if isinstance(event_object, MessageObj):
            obj_message = event_object.message
            obj_reactions = event_object.reactions
            obj_details = event_object.details
            obj_attachments = event_object.attachments
            print(f"##### event_object: MessageObject:\n"
                  f"\tobject: {event_object}\n"
                  f"\tmessage: {obj_message}\n"
                  f"\treactions: {obj_reactions}\n"
                  f"\tdetails: {obj_details}\n"
                  f"\tattachments: {obj_attachments}\n")
        elif isinstance(event_object, AuthObj):
            print(f"##### event_object: AuthObject")
        elif isinstance(event_object, ConversationObj):
            obj_sender_name = event_object.sender_name
            obj_sender_phone = event_object.sender_phone
            obj_provider = event_object.provider
            print(f"##### event_object: ConversationObject:\n"
                  f"\tobject: {event_object}\n"
                  f"\tsender_name: {obj_sender_name}\n"
                  f"\tsender_phone: {obj_sender_phone}\n"
                  f"\tprovider: {obj_provider}\n")
        else:
            print(f"##### event_object: Unknown Object:\n"
                  f"type(event_object): {type(event_object)}"
                  f"\tobject: {event_object}\n"
                  f"event_object")

    json_content = {"Message": "Webhook [OK]"}
    json_response = JSONResponse(
        content=json_content,
        status_code=status.HTTP_200_OK)
    return json_response
