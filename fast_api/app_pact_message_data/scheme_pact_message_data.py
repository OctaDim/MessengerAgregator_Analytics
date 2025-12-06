from typing import Optional

from pydantic import BaseModel


class InMessageDataByMessageId(BaseModel):
    pact_api_token: Optional[str]
    company_id: str
    conversation_id: str
    message_id: str
    page_number: Optional[int]
    items_per_page: Optional[int]
    pact_api_timeout: Optional[float]
