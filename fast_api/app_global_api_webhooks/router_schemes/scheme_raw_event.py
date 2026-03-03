from typing import Literal

from fast_api.app_global_api_webhooks.router_schemes.scheme_base_event_data import (
    BaseEventData)


class RawData(BaseEventData):
    event_type: Literal["Raw"]
