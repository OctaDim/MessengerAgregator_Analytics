from typing import Optional, Union, Literal, Self

from pydantic import BaseModel, model_validator, Field

from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_callback_query import (
    CallbackQueryData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_chat_action import (
    ChatActionData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_inline_query import (
    InlineQueryData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_message_deleted import (
    MessageDeletedData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_message_edited import (
    MessageEditedData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_message_read import (
    MessageReadData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_new_message import (
    NewMessageData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_new_message_client_sent import (
    ClientSentNewMessageData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_raw_event import (
    RawData)
from fast_api.app_global_api_webhooks.pydantic_schemes.scheme_user_update import (
    UserUpdateData)


class GlobalApiWebhookData(BaseModel):
    event_data: Optional[
        Union[
            NewMessageData,
            ClientSentNewMessageData,
            MessageEditedData,
            MessageReadData,
            MessageDeletedData,
            ChatActionData,
            UserUpdateData,
            CallbackQueryData,
            InlineQueryData,
            RawData]] = Field(discriminator="event_type")
    source: Optional[Union[str, Literal["telegram_tlt"]]]
    operation: Optional[Union[str, Literal["test"]]]

    # # Validation in router to fix recursion error
    # def __init__(self, **data: Any) -> None:
    #     validate_log_pydantic_obj_errors(PydanticBaseModel=self.__class__,
    #                                      request_json=data)
    #     super().__init__(**data)

    @model_validator(mode="before")
    def validate_basemodel_obj(cls, data: dict) -> dict | None:
        # # Validation in router to fix recursion error
        # validate_log_pydantic_obj_errors(PydanticBaseModel=self.__class__,
        #                                  request_json=self.model_dump())
        has_group_1_flag = all([data["event_data"], data["source"]])
        has_group_2_flag = all([data["source"], data["operation"]])
        if not (has_group_1_flag or has_group_2_flag):  # Both are False
            error_log = (
                f"PYDANTIC COMBINATIONS [ERROR]: "
                f"group 1 (event_data, source) OR "
                f"group 2 (source, operation) needed\n"
                f"has_group_1_flag: {has_group_1_flag}\n"
                f"has_group_2_flag: {has_group_1_flag}\n"
                f"\tevent_data: {data["event_data"]}\n"
                f"\tsource: {data["source"]}\n"
                f"\toperation: {data["operation"]}\n")
            print(error_log)
            raise ValueError(error_log)
        else:  # has_group_1_flag or has_group_2_flag
            return data
