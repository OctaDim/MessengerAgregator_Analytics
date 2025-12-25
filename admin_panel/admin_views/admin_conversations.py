from datetime import datetime

from sqladmin import ModelView
from starlette.requests import Request

from admin_panel.admin_views.mixin_update_model_old_pk_val import (
    OldPrimKeyNewDataMixin)
from admin_panel.custom_actions_mixins.mix_cancel_all_filters import (
    CanceAllFiltersSortsMixin)
from admin_panel.custom_classes.custom_filter_classes import (
    CustomBooleanFilter, CustomRepliedStateFilter,
    CustomStaticStringsFilter, CustomStaticNumbersFilter)
from configs.labels_messages import LABELS
from db_postgres.postgres_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_queries.qry_sync_get_conversations_filter_values import (
    get_sync_conversation_filters_values_qry)


class ConversationsAdmin(ModelView,
                         CanceAllFiltersSortsMixin,
                         OldPrimKeyNewDataMixin,
                         model=WebhookConversationModel):
    name = LABELS.CONVERSATION_PANEL_TITLE
    name_plural = LABELS.CONVERSATIONS_PANEL_TITLE
    icon = LABELS.ICON
    category = LABELS.CONVERSATIONS_CATEGORY_TITLE
    category_icon = LABELS.CONVERSATIONS_CATEGORY_ICON
    is_async = True  # Default False
    page_size = 200
    page_size_options = [25, 50, 100, 200, 500, 1000]
    can_create = False  # Some bug: if not displayed or hidden, change can_export to False, restart, then True, restart
    can_delete = False
    can_edit = True
    can_view_details = True
    can_export = True

    column_list = [  # Main table columns
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,  #
        WebhookConversationModel.sender_name,  #
        WebhookConversationModel.sender_phone,  #
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,  #
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  #
        WebhookConversationModel.group,  #
        # WebhookConversationModel.created_at,
        WebhookConversationModel.last_updated_at,
        # WebhookConversationModel.active,
        # WebhookConversationModel.local_created_at,
        # WebhookConversationModel.local_updated_at,
    ]

    column_labels = {  # Human labels instead of table fields names
        WebhookConversationModel.local_id: LABELS.LOCAL_ID,
        WebhookConversationModel.chats_subject_id: LABELS.CHATS_SUBJECT_ID,
        WebhookConversationModel.this_conversation_subject: LABELS.THIS_CONVERSATION_SUBJECT,
        WebhookConversationModel.event: LABELS.EVENT,
        WebhookConversationModel.type: LABELS.TYPE,
        WebhookConversationModel.id: LABELS.ID,
        WebhookConversationModel.company_id: LABELS.COMPANY_ID,
        WebhookConversationModel.sender_name: LABELS.SENDER_NAME,
        WebhookConversationModel.sender_phone: LABELS.SENDER_PHONE,
        WebhookConversationModel.sender_external_id: LABELS.SENDER_EXTERNAL_ID,
        WebhookConversationModel.sender_external_public_id: LABELS.SENDER_EXTERNAL_PUBLIC_ID,
        WebhookConversationModel.provider: LABELS.PROVIDER,
        WebhookConversationModel.avatar_url: LABELS.AVATAR_URL,
        WebhookConversationModel.last_message_id: LABELS.LAST_MESSAGE_ID,
        WebhookConversationModel.operational_state: LABELS.OPERATIONAL_STATE,
        WebhookConversationModel.replied_state: LABELS.REPLIED_STATE,
        WebhookConversationModel.group: LABELS.GROUP,
        WebhookConversationModel.created_at: LABELS.CREATED_AT,
        WebhookConversationModel.last_updated_at: LABELS.UPDATED_AT,
        WebhookConversationModel.active: LABELS.ACTIVE,
        WebhookConversationModel.local_created_at: LABELS.LOCAL_CREATED,
        WebhookConversationModel.local_updated_at: LABELS.LOCAL_UPDATED,
    }

    column_searchable_list = [  # Search included fields
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,  #
        WebhookConversationModel.sender_name,  #
        WebhookConversationModel.sender_phone,  #
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,  #
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  #
        WebhookConversationModel.group,  #
        WebhookConversationModel.created_at,
        WebhookConversationModel.last_updated_at,
        # WebhookConversationModel.active,
        # WebhookConversationModel.local_created_at,
        # WebhookConversationModel.local_updated_at,
    ]

    @property
    def column_filters(self):  # Ordinal and custom filters to filter column list
        filters_values = get_sync_conversation_filters_values_qry()  # All possible unique and sorted values for filters
        providers_values = filters_values["provider_values"]
        company_id_values = filters_values["company_id_values"]

        column_filters_list = [
            # Filter using custom overridden filter class for boolean field
            CustomBooleanFilter(  # field: WebhookConversationModel.group
                column=WebhookConversationModel.group,
                title=LABELS.GROUP),

            # Filter using custom overridden filter class for string field
            CustomRepliedStateFilter(  # field: WebhookConversationModel.replied_state
                column=WebhookConversationModel.replied_state,
                values=[],  # Defined in overridden CustomRepliedStateFilter and 'def lookups', can be defined here
                title=LABELS.REPLIED_FILTER_TITLE),

            # Filter using custom overridden filter class for string field
            CustomStaticStringsFilter(  # field: WebhookConversationModel.provider
                column=WebhookConversationModel.provider,
                values=providers_values,
                title=LABELS.PROVIDER_FILTER_TITLE),

            # Filter using custom overridden filter class for string field
            CustomStaticNumbersFilter(  # field: draft_category
                column=WebhookConversationModel.company_id,
                values=company_id_values,
                title=LABELS.COMPANY_ID_FILTER_TITLE),

            # Filter using custom overridden filter class for property model field
            # CustAccountDataFilter(  # combine fields: account_username, account_id
            #     column=WebhookConversationModel.account_data,
            #     values=acc_data_values,
            #     title=LABELS.FILTER_ACCOUNT_DATA),

            # CustomNewCategoryTextFilter(  # combine fields: new_category, new_text
            #     column=WebhookConversationModel.new_category,
            #     values=[("all", LABELS.ALL_RECS),
            #             ("new_category", LABELS.NEW_CLASS_ONLY),
            #             ("new_text", LABELS.NEW_TEXT_ONLY),
            #             ("new_category_text", LABELS.NEW_CLASS_AND_TEXT)],
            #     title=LABELS.FILTER_NEW_DRAFT),

            # CustomStaticValuesFilter(  # field: account_username
            #     column=WebhookConversationModel.account_username,
            #     values=username_values,
            #     title=LABELS.FILTER_ACCOUNT_USERNAME),

            # CustomStaticValuesFilter(  # field: account_id
            #     column=WebhookConversationModel.account_id,
            #     values=acc_id_values,
            #     title=LABELS.ACCOUNT_ID),

            # CustomForeignKeyFilter(  # foreign key field: customer_id (display field: account_id)
            #     foreign_key=WebhookConversationModel.customer_id,
            #     foreign_display_field=CustomerModel.account_username,
            #     foreign_model=CustomerModel,
            #     title=LABELS.FILTER_ACCOUNT_USERNAME),

            # CustomForeignKeyFilter(  # foreign key field: customer_id (display field: account_id)
            #     foreign_key=WebhookConversationModel.customer_id,
            #     foreign_display_field=CustomerModel.account_id,
            #     foreign_model=CustomerModel,
            #     title=LABELS.FILTER_ACCOUNT_ID),

        ]  # <== Do not remove or comment!!! It's used!!!
        return column_filters_list

    column_default_sort = [
        (WebhookConversationModel.local_id, True),  # True - descending, False - ascending
        (WebhookConversationModel.active, False),  # True - descending, False - ascending
    ]

    column_sortable_list = [  # Column list (main table) sortable fields
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,  #
        WebhookConversationModel.sender_name,  #
        WebhookConversationModel.sender_phone,  #
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,  #
        WebhookConversationModel.provider,
        WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  #
        WebhookConversationModel.group,  #
        WebhookConversationModel.created_at,
        WebhookConversationModel.last_updated_at,
        WebhookConversationModel.active,
        WebhookConversationModel.local_created_at,
        WebhookConversationModel.local_updated_at,
    ]

    column_details_list = [  # Display form fields, all fields if not defined
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,  #
        WebhookConversationModel.sender_name,  #
        WebhookConversationModel.sender_phone,  #
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,  #
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  #
        WebhookConversationModel.group,  #
        WebhookConversationModel.created_at,
        WebhookConversationModel.last_updated_at,
        # WebhookConversationModel.active,
        # WebhookConversationModel.local_created_at,
        # WebhookConversationModel.local_updated_at,
    ]

    # column_details_exclude_list = [  # If column_details_list not defined, all fields except defined
    #     WebhookConversationModel.local_created_at,
    #     WebhookConversationModel.local_updated_at, ]

    form_columns = [  # Edit form fields, all fields if not defined
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        # WebhookConversationModel.event,  ##
        # WebhookConversationModel.type,  ##
        # WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,  #
        WebhookConversationModel.sender_name,  #
        WebhookConversationModel.sender_phone,  #
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,  #
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,  ##
        # WebhookConversationModel.last_message_id,  ##
        # WebhookConversationModel.operational_state,  ##
        # WebhookConversationModel.replied_state,  #
        WebhookConversationModel.group,  #
        # WebhookConversationModel.created_at,
        # WebhookConversationModel.last_updated_at,
        # WebhookConversationModel.active,
        # WebhookConversationModel.local_created_at,
        # WebhookConversationModel.local_updated_at,
    ]

    # form_excluded_columns = [  # If form_columns not defined
    #     "id",
    #     "created_at",
    #     "updated_at",
    #     "creation_reason", ]

    form_include_pk = True  # Display primary key fields in edit form or not

    # form_overrides = {
    #     # See all possible fields types in:
    #     # from wtforms.fields.choices
    #     # from wtforms.fields.core
    #     # from wtforms.fields.datetime
    #     # from wtforms.fields.form
    #     # from wtforms.fields.list
    #     # from wtforms.fields.numeric
    #     # from wtforms.fields.simple
    #     # from wtforms.utils import unset_value
    #     "this_conversation_subject": QuerySelectField,
    # }

    form_widget_args = {  # Edit form fields additional properties
        # "local_id": {"readonly": True, "disabled": True},
        "chats_subject_id": {"disabled": True},
        "company_id": {"disabled": True},
        "sender_name": {"disabled": True},
        "sender_phone": {"disabled": True},
        "sender_external_id": {"disabled": True},
        "sender_external_public_id": {"disabled": True},
        "provider": {"disabled": True},
        "group": {"disabled": True},
        "created_at": {"disabled": True},
        # "active": {"disabled": True},
        "last_updated_at": {"disabled": True},
        "local_created_at": {"disabled": True},
        "local_updated_at": {"disabled": True}, }

    # form_ajax_refs = {
    #     "this_conversation_subject": {
    #         "fields": ("chats_subject_name", "id"),
    #         "order_by": "chats_subject_name",
    #         "page_size": 10}}

    # Preserve changing local_id via request or via editable form field
    # Some other functionality can be defined here on update
    async def update_model(self, request: Request, pk: str, data: dict) -> None:
        data_with_old_pk = await self.set_old_pkey_in_new_data(
            prim_key_value_str=pk,
            prim_key_name="local_id",
            form_data=data)
        return await super().update_model(request, pk, data=data_with_old_pk)

    @staticmethod
    # used by column_formatters/column_formatters_detail bellow, multi fields operations
    # model_obj = cur record, attribute = field string name
    def format_datetime_fields(model_obj, attribute):
        field_value = getattr(model_obj, attribute)
        if field_value and isinstance(field_value, datetime):
            formated_datetime = field_value.strftime("%d-%m-%Y %H:%M")
            return formated_datetime
        elif not field_value:
            return ""
        else:
            return field_value

    @staticmethod
    # used by column_formatters/column_formatters_detail bellow, single field operation
    # model_obj = cur record, attribute = field string name
    def format_replied_state_field(model_obj, attribute):
        replied_states_labels = {
            "replied": LABELS.REPLIED_FILTER_LABEL,
            "unreplied": LABELS.UNREPLIED_FILTER_LABEL}
        field_value = getattr(model_obj, attribute)
        display_value = replied_states_labels.get(field_value)
        if display_value:
            return display_value
        elif not display_value:
            return ""
        else:
            return field_value

    @staticmethod
    # used by column_formatters/column_formatters_detail bellow, single field operation
    # model_obj = cur record, attribute = field string name
    def format_subject_name_field(model_obj, attribute):
        model_obj = getattr(model_obj, attribute)
        if model_obj and hasattr(model_obj, 'chats_subject_name'):
            return model_obj.chats_subject_name
        return ""

    # @staticmethod
    # def format_created_at(model_obj, attribute):  # as example
    #     # used by column_formatters/column_formatters_detail bellow
    #     # model_obj = cur record, attribute = field string name
    #     if model_obj.created_at:  # Single field operations, as example
    #         formated_data = model_obj.created_at.strftime("%d-%m-%Y %H:%M")
    #     else:
    #         return None

    # @staticmethod
    # # used by column_formatters/column_formatters_detail bellow
    # # model_obj = cur record, attribute = field string name
    # def format_current_status(model, attribute):  # as example
    #     list_display_value = model.current_status.value  # Enum values instead of attr names
    #     return list_display_value

    column_formatters = {
        WebhookConversationModel.created_at: format_datetime_fields,
        WebhookConversationModel.last_updated_at: format_datetime_fields,
        WebhookConversationModel.local_created_at: format_datetime_fields,
        WebhookConversationModel.local_updated_at: format_datetime_fields,
        WebhookConversationModel.replied_state: format_replied_state_field,
        WebhookConversationModel.this_conversation_subject: format_subject_name_field,
        # WebhookConversationModel.current_status: format_created_at,  # as example for single field
        # WebhookConversationModel.current_status: format_current_status,  # as example for enum field
    }

    column_formatters_detail = {
        WebhookConversationModel.created_at: format_datetime_fields,
        WebhookConversationModel.last_updated_at: format_datetime_fields,
        WebhookConversationModel.local_created_at: format_datetime_fields,
        WebhookConversationModel.local_updated_at: format_datetime_fields,
        WebhookConversationModel.replied_state: format_replied_state_field,
        WebhookConversationModel.this_conversation_subject: format_subject_name_field,
        # WebhookConversationModel.current_status: format_created_at,  # as example for single field
        # WebhookConversationModel.current_status: format_current_status,  # as example for enum field
    }

    # def can_view_details(self, request: Request) -> bool:
    #     return False
    #
    # def can_create(self, request: Request) -> bool:
    #     return False
    #
    # def can_edit(self, request: Request) -> bool:
    #     return False
    #
    # def can_delete(self, request: Request) -> bool:
    #     return False
