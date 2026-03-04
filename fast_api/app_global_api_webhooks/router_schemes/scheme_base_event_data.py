from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseEventData(BaseModel):
    model_config = ConfigDict(frozen=True)

    event_type: str
    web_account_id: str
    web_account_username: str
    tlt_account_type: str
    tlt_phone: Optional[str]
    tlt_bot_token: Optional[str]

    action: Optional[str]
