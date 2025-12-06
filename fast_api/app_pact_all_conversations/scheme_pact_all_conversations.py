from typing import Optional

from pydantic import BaseModel


class InPactAllConversations(BaseModel):
    pact_api_token: Optional[str]
    company_id: str
    page_number: Optional[int]
    items_per_page: Optional[int]
    pact_api_timeout: Optional[float]
