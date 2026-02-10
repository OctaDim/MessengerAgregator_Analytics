from datetime import datetime
from typing import Optional, Union, Literal, Self, Any

from pydantic import (
    BaseModel, Field, model_validator)

from utils_common.validate_log_pydantic_errors import (
    validate_log_pydantic_obj_errors)


class MessageObject(BaseModel):
    id: int
    external_id: Optional[str]
    company_id: int
    conversation_id: Optional[int]
    contact_id: Optional[int]
    replied_to_id: Optional[int]
    created_at: datetime
    external_created_at: Optional[datetime]
    income: Optional[bool]
    status: Optional[str]
    message: Optional[str]
    reactions: Optional[list] = Field(default_factory=list)
    details: Optional[dict] = Field(default_factory=dict)
    attachments: Optional[list] = Field(default_factory=list)


class AuthObject(BaseModel):
    id: int
    company_id: int
    provider: str
    state: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    sync_messages_at: Optional[datetime]


class ConversationObject(BaseModel):
    id: int
    company_id: int
    sender_name: str
    sender_phone: Optional[str]
    sender_external_id: str
    sender_external_public_id: Optional[str]
    provider: str
    avatar_url: str
    created_at: datetime
    last_updated_at: datetime
    last_message_id: int
    operational_state: str
    replied_state: str
    group: bool


class PactWebhookData(BaseModel):
    event: str = None
    type: str = None
    object: Union[MessageObject, AuthObject, ConversationObject] = None
    source: Union[Literal["pact.im"], str] = None
    operation: Union[Literal["test"], str] = None

    # def __init__(self, **data: Any) -> None:
    #     validate_log_pydantic_obj_errors(
    #         PydanticBaseModel=self.__class__, request_json=data)
    #     super().__init__(**data)

    @model_validator(mode="after")
    def validate_basemodel_obj(self) -> Self:
        # validate_log_pydantic_obj_errors(PydanticBaseModel=self.__class__,
        #                                  request_json=self.model_dump())

        has_group_1_flag = all([self.event, self.type, self.object])
        has_group_2_flag = all([self.event, self.type])
        has_group_3_flag = all([self.source, self.operation])

        if not (has_group_1_flag or has_group_2_flag or has_group_3_flag):
            error_log = (
                f"PYDANTIC COMBINATIONS [ERROR]: "
                f"group 1 (event, type, object) OR "
                f"group 2 (event, type) OR "
                f"group 3 (source, operation) needed\n"
                f"has_group_1_flag: {has_group_1_flag}\n"
                f"has_group_2_flag: {has_group_1_flag}\n"
                f"has_group_3_flag: {has_group_3_flag}\n"
                f"\tevent: {self.event}\n"
                f"\ttype: {self.type}\n"
                f"\tobject: {self.object}\n"
                f"\tsource: {self.source}\n"
                f"\toperation: {self.operation}\n")
            print(error_log)
            raise ValueError(error_log)
        else:  # has_group_1_flag or has_group_2_flag
            return self
