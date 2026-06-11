from fastapi import HTTPException
from pydantic import BaseModel, model_validator
from starlette import status


class InTelegramContactData(BaseModel):
    username_cst: str | None = None
    phone_cst: str | None = None
    first_name_cst: str | None = None
    last_name_cst: str | None = None

    @model_validator(mode="after")
    def validate_contact_fields(self):
        has_contact_field = any([
            bool(self.username_cst),
            bool(self.phone_cst),
            bool(self.first_name_cst),
            bool(self.last_name_cst),
        ])
        if not has_contact_field:
            error_log = (
                f"\nEmpty telegram contact data passed [ERROR]:\n"
                f"Possible combinations: any of "
                f"[username_cst, phone_cst, first_name_cst, last_name_cst]\n"
                f"username_cst: {self.username_cst}\n"
                f"phone_cst: {self.phone_cst}\n"
                f"first_name_cst: {self.first_name_cst}\n"
                f"last_name_cst: {self.last_name_cst}\n")
            print(error_log)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=error_log)
        return self


class InMessagesByContactsPagination(BaseModel):
    current_page: int | None
    messages_per_page: int | None
    tlt_config_name: str | None = None
    telegram_contacts: list[InTelegramContactData]

    @model_validator(mode="after")
    def validate_request_fields(self):
        if not self.telegram_contacts:
            error_log = (f"\nEmpty telegram contacts list passed [ERROR]:\n"
                         f"telegram_contacts: {self.telegram_contacts}\n")
            print(error_log)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=error_log)

        if self.current_page is not None and self.current_page < 1:
            error_log = (f"\nInvalid current_page passed [ERROR]:\n"
                         f"current_page: {self.current_page}\n")
            print(error_log)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=error_log)

        if self.messages_per_page is not None and self.messages_per_page < 1:
            error_log = (f"\nInvalid messages_per_page passed [ERROR]:\n"
                         f"messages_per_page: {self.messages_per_page}\n")
            print(error_log)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=error_log)
        return self

