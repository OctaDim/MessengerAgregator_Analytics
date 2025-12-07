from typing import Optional, Literal

from pydantic import BaseModel, Field


class InPactAllCompanies(BaseModel):
    pact_api_token: Optional[str]
    last_req_next_page_token: Optional[str]
    items_per_page: Optional[int] = Field(ge=1, le=100, default=100)
    sort_direction: Optional[Literal["asc", "desc"]] = "asc"
    pact_api_timeout: Optional[float]
