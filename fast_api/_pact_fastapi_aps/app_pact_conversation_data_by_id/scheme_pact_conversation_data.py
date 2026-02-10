from typing import Optional

from pydantic import BaseModel

from configs.settings import PACT_WEBHOOKS_OPTIONS


class InConversDataByConversID(BaseModel):
    pact_api_token: Optional[str]
    company_id: int
    conversation_id: int
    pact_api_timeout: Optional[float] = PACT_WEBHOOKS_OPTIONS.OUTGOING_EXT_API_REQ_TIMEOUT
