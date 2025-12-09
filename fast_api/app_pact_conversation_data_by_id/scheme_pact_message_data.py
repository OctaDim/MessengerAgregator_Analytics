from typing import Optional

from pydantic import BaseModel


class InConversDataByConverseId(BaseModel):
    pact_api_token: Optional[str]
    company_id: str
    conversation_id: str
    pact_api_timeout: Optional[float]
