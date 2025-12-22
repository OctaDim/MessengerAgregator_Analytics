from typing import Optional

from pydantic import BaseModel

from configs.settings import WEBHOOKS_OPTIONS


class InPactAllConversations(BaseModel):
    pact_api_token: Optional[str]
    company_id: str
    page_number: Optional[int]
    items_per_page: Optional[int]
    pact_api_timeout: Optional[float] = WEBHOOKS_OPTIONS.OUTGOING_EXT_API_REQ_TIMEOUT
