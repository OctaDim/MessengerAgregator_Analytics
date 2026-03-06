from typing import Literal

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_base_event_data import (
    BaseEventData)


class CallbackQueryData(BaseEventData):
    event_type: Literal["CallbackQuery"]  # discriminator="CallbackQuery"
