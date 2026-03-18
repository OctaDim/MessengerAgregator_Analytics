from pydantic import BaseModel

from configs.settings import GLOBAL_API_WEBHOOKS_OPTIONS


class InAllMessagesPagination(BaseModel):
    current_page: int | None
    messages_per_page: int | None
