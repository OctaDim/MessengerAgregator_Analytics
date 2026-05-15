from typing import Literal

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_new_message import (
    NewMessageData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_s3_additional_data import (
    S3AdditionalData)


class ClientSentNewMessageData(NewMessageData, S3AdditionalData):
    event_type: Literal["ClientSentNewMessage"]  # discriminator="ClientSentNewMessage"
