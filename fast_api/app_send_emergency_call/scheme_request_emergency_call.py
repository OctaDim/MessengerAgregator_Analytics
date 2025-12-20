from typing import Optional

from pydantic import BaseModel


class InWarningCallData(BaseModel):
    company_uuid: str
