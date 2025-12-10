from typing import Optional

from pydantic import BaseModel

from configs.settings import WEBHOOKS_OPTIONS


class InAllMessagesByConversation(BaseModel):
    pact_api_token: Optional[str]
    company_id: str
    conversation_id: str
    page_number: Optional[int]
    items_per_page: Optional[int]
    pact_api_timeout: Optional[float] = WEBHOOKS_OPTIONS.OUTGOING_EXT_API_REQUEST_TIMEOUT
