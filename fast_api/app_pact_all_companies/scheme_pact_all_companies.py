from typing import Optional, Literal

from pydantic import BaseModel, Field

from configs.settings import WEBHOOKS_OPTIONS


class InPactAllCompanies(BaseModel):
    pact_api_token: Optional[str]
    last_req_next_page_token: Optional[str]
    items_per_page: Optional[int] = Field(ge=1, le=100, default=100)
    sort_direction: Optional[Literal["asc", "desc"]] = "asc"
    pact_api_timeout: Optional[float] = WEBHOOKS_OPTIONS.OUTGOING_EXT_API_REQUEST_TIMEOUT
