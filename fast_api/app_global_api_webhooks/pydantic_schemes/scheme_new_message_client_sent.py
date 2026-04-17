from typing import Literal

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_new_message import (
    NewMessageData)


class ClientSentNewMessageData(NewMessageData):
    event_type: Literal["ClientSentNewMessage"]  # discriminator="ClientSentNewMessage"
