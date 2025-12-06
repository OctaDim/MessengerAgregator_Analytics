from datetime import datetime
from typing import Optional, List, Union, Dict, Literal, Self

from pydantic import (
    BaseModel, Field, model_validator)


class MessageObj(BaseModel):
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
    reactions: List = Field(default_factory=list)
    details: Dict = Field(default_factory=dict)
    attachments: List = Field(default_factory=list)


class AuthObj(BaseModel):
    id: int
    company_id: int
    provider: str
    state: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    sync_messages_at: Optional[datetime]


class ConversationObj(BaseModel):
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
    object: Union[MessageObj, AuthObj, ConversationObj] = None
    source: Union[Literal["pact.im"], str] = None
    operation: Union[Literal["test"], str] = None

    @model_validator(mode="after")
    def validate_basemodel_obj(self) -> Self:
        has_group_1_flag = all([self.event, self.type, self.object])
        has_group_2_flag = all([self.source, self.operation])

        if not (has_group_1_flag or has_group_2_flag):
            error_log = (f"PYDANTIC COMBINATIONS [ERROR]: "
                         f"(event, type, object) OR (source, operation) needed\n"
                         f"has_group_1_flag: {has_group_1_flag}\n"
                         f"\tevent: {self.event}\n"
                         f"\ttype: {self.type}\n"
                         f"\tobject: {self.object}\n"
                         f"has_group_2_flag: {has_group_1_flag}\n"
                         f"\ttype: {self.type}\n"
                         f"\tobject: {self.object}\n")
            print(error_log)
            raise ValueError(error_log)
        else:  # has_group_1_flag or has_group_2_flag
            return self
