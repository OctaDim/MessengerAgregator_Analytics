from typing import Optional, Literal

from pydantic import BaseModel, Field

from configs.settings import PACT_WEBHOOKS_OPTIONS


class InPactAllCompanies(BaseModel):
    pact_api_token: Optional[str]
    last_req_next_page_token: Optional[str] = None
    items_per_page: Optional[int] = Field(ge=1, le=100, default=1000)
    sort_direction: Optional[Literal["asc", "desc"]] = "asc"
    pact_api_timeout: Optional[float] = PACT_WEBHOOKS_OPTIONS.OUTGOING_EXT_API_REQ_TIMEOUT
