from datetime import datetime

from sqladmin import ModelView
from starlette.requests import Request

from admin_panel.admin_views.mixin_set_new_data_old_pk import (
    OldPrimKeyNewDataMixin)
from admin_panel.custom_actions_mixins._pact_custom_actions.mix_cancel_all_filters import (
    CanceAllFiltersSortsMixin)
from admin_panel.custom_classes._pact_custom_classes.custom_filter_classes import (
    CustomBooleanFilter, CustomRepliedStateFilter,
    CustomStaticStringsFilter, CustomStaticNumbersFilter,
    CustomForeignKeyFilter)
from configs.labels_messages import PACT_LABELS
from configs.settings import PACT_SQLADMIN_OPTIONS
from db_postgres.postgres_models._pact_pgs_models.chats_subjects_model import (
    ChatsSubjectModel)
from db_postgres.postgres_models._pact_pgs_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_queries._pact_pgs_queries.qry_sync_get_conversations_filter_values import (
    get_sync_conversation_filters_values_qry)


class ConversationsAdmin(ModelView,
                         CanceAllFiltersSortsMixin,
                         OldPrimKeyNewDataMixin,  # Update mixin
                         model=WebhookConversationModel):
    name = PACT_LABELS.CONVERSATION_PANEL_TITLE
    name_plural = PACT_LABELS.CONVERSATIONS_PANEL_TITLE
    icon = PACT_LABELS.ICON
    category = PACT_LABELS.CONVERSATIONS_CATEGORY_TITLE
    category_icon = PACT_LABELS.CONVERSATIONS_CATEGORY_ICON
    is_async = True  # Default False
    page_size = 200
    page_size_options = [25, 50, 100, 200, 500, 1000]
    can_create = True  # Some bug: if not displayed or hidden, change can_export to False, restart, then True, restart
    can_delete = False
    can_edit = True
    can_view_details = True
    can_export = True

    column_list = [  # Main table columns
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,  # Display relation fld links. If commented => lazy load err
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,
        WebhookConversationModel.sender_name,
        WebhookConversationModel.sender_phone,
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  ##
        WebhookConversationModel.group,
        # WebhookConversationModel.created_at,  ##
        WebhookConversationModel.last_updated_at,  ##
        WebhookConversationModel.active,  ##
        # WebhookConversationModel.local_created_at,  ##
        # WebhookConversationModel.local_updated_at,  ##
    ]

    column_labels = {  # Human labels instead of table fields names
        WebhookConversationModel.local_id: PACT_LABELS.LOCAL_ID,
        WebhookConversationModel.chats_subject_id: PACT_LABELS.CHATS_SUBJECT_NAME_BY_ID,
        WebhookConversationModel.this_conversation_subject: PACT_LABELS.CHATS_SUBJECT_LINK,
        WebhookConversationModel.event: PACT_LABELS.EVENT,
        WebhookConversationModel.type: PACT_LABELS.TYPE,
        WebhookConversationModel.id: PACT_LABELS.ID,
        WebhookConversationModel.company_id: PACT_LABELS.COMPANY_ID,
        WebhookConversationModel.sender_name: PACT_LABELS.SENDER_NAME,
        WebhookConversationModel.sender_phone: PACT_LABELS.SENDER_PHONE,
        WebhookConversationModel.sender_external_id: PACT_LABELS.SENDER_EXTERNAL_ID,
        WebhookConversationModel.sender_external_public_id: PACT_LABELS.SENDER_EXTERNAL_PUBLIC_ID,
        WebhookConversationModel.provider: PACT_LABELS.PROVIDER,
        WebhookConversationModel.avatar_url: PACT_LABELS.AVATAR_URL,
        WebhookConversationModel.last_message_id: PACT_LABELS.LAST_MESSAGE_ID,
        WebhookConversationModel.operational_state: PACT_LABELS.OPERATIONAL_STATE,
        WebhookConversationModel.replied_state: PACT_LABELS.REPLIED_STATE,
        WebhookConversationModel.group: PACT_LABELS.GROUP,
        WebhookConversationModel.created_at: PACT_LABELS.CREATED_AT,
        WebhookConversationModel.last_updated_at: PACT_LABELS.UPDATED_AT,
        WebhookConversationModel.active: PACT_LABELS.ACTIVE,
        WebhookConversationModel.local_created_at: PACT_LABELS.LOCAL_CREATED,
        WebhookConversationModel.local_updated_at: PACT_LABELS.LOCAL_UPDATED,
    }

    column_searchable_list = [  # Search included fields
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,
        WebhookConversationModel.sender_name,
        WebhookConversationModel.sender_phone,
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,
        WebhookConversationModel.provider,
        WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  ##
        WebhookConversationModel.group,
        WebhookConversationModel.created_at,  ##
        WebhookConversationModel.last_updated_at,  ##
        WebhookConversationModel.active,  ##
        WebhookConversationModel.local_created_at,  ##
        WebhookConversationModel.local_updated_at,  ##
    ]

    @property
    def column_filters(self):  # Ordinal and custom filters to filter column list
        filters_values = get_sync_conversation_filters_values_qry()  # Custom unique and sorted values for filters
        providers_values = filters_values["provider_values"]
        company_id_values = filters_values["company_id_values"]

        column_filters_list = [
            # Filter using custom overridden filter class for boolean field
            CustomBooleanFilter(  # field: WebhookConversationModel.group
                column=WebhookConversationModel.group,
                title=PACT_LABELS.GROUP),

            # Filter using custom overridden filter class for string field
            CustomRepliedStateFilter(  # field: WebhookConversationModel.replied_state
                column=WebhookConversationModel.replied_state,
                values=[],  # Defined in overridden CustomRepliedStateFilter and 'def lookups', can be defined here
                title=PACT_LABELS.REPLIED_FILTER_TITLE),

            # Filter using custom overridden filter class for string field
            CustomStaticStringsFilter(  # field: WebhookConversationModel.provider
                column=WebhookConversationModel.provider,
                values=providers_values,
                title=PACT_LABELS.PROVIDER_FILTER_TITLE),

            # Filter using custom overridden filter class for string field
            CustomStaticNumbersFilter(  # field: draft_category
                column=WebhookConversationModel.company_id,
                values=company_id_values,
                title=PACT_LABELS.COMPANY_ID_FILTER_TITLE),

            CustomForeignKeyFilter(  # foreign key field: customer_id (display field: account_id)
                foreign_key=WebhookConversationModel.chats_subject_id,
                foreign_display_field=ChatsSubjectModel.chats_subject_name,
                foreign_model=ChatsSubjectModel,
                title=PACT_LABELS.CHATS_SUBJECT_NAME_BY_ID),

            # Filter using custom overridden filter class for property model field
            # CustAccountDataFilter(  # combine fields: account_username, account_id
            #     column=WebhookConversationModel.account_data,
            #     values=acc_data_values,
            #     title=PACT_LABELS.FILTER_ACCOUNT_DATA),

            # CustomNewCategoryTextFilter(  # combine fields: new_category, new_text
            #     column=WebhookConversationModel.new_category,
            #     values=[("all", PACT_LABELS.ALL_RECS),
            #             ("new_category", PACT_LABELS.NEW_CLASS_ONLY),
            #             ("new_text", PACT_LABELS.NEW_TEXT_ONLY),
            #             ("new_category_text", PACT_LABELS.NEW_CLASS_AND_TEXT)],
            #     title=PACT_LABELS.FILTER_NEW_DRAFT),

            # CustomStaticValuesFilter(  # field: account_username
            #     column=WebhookConversationModel.account_username,
            #     values=username_values,
            #     title=PACT_LABELS.FILTER_ACCOUNT_USERNAME),

            # CustomStaticValuesFilter(  # field: account_id
            #     column=WebhookConversationModel.account_id,
            #     values=acc_id_values,
            #     title=PACT_LABELS.ACCOUNT_ID),

            # CustomForeignKeyFilter(  # foreign key field: customer_id (display field: account_id)
            #     foreign_key=WebhookConversationModel.customer_id,
            #     foreign_display_field=CustomerModel.account_username,
            #     foreign_model=CustomerModel,
            #     title=PACT_LABELS.FILTER_ACCOUNT_USERNAME),

            # CustomForeignKeyFilter(  # foreign key field: customer_id (display field: account_id)
            #     foreign_key=WebhookConversationModel.customer_id,
            #     foreign_display_field=CustomerModel.account_id,
            #     foreign_model=CustomerModel,
            #     title=PACT_LABELS.FILTER_ACCOUNT_ID),

        ]  # <== Do not remove or comment!!! It's used!!!
        return column_filters_list

    column_default_sort = [
        (WebhookConversationModel.local_id, True),  # True - descending, False - ascending
        (WebhookConversationModel.active, False),  # True - descending, False - ascending
    ]

    column_sortable_list = [  # Column list (main table) sortable fields
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        # WebhookConversationModel.this_conversation_subject,  # Excluded because relation field sorting error
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,
        WebhookConversationModel.sender_name,
        WebhookConversationModel.sender_phone,
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,
        WebhookConversationModel.provider,
        WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  ##
        WebhookConversationModel.group,
        WebhookConversationModel.created_at,  ##
        WebhookConversationModel.last_updated_at,  ##
        WebhookConversationModel.active,  ##
        WebhookConversationModel.local_created_at,  ##
        WebhookConversationModel.local_updated_at,  ##
    ]

    column_details_list = [  # Display form fields, all fields if not defined
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,
        WebhookConversationModel.sender_name,
        WebhookConversationModel.sender_phone,
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  ##
        WebhookConversationModel.group,
        WebhookConversationModel.created_at,  ##
        WebhookConversationModel.last_updated_at,  ##
        WebhookConversationModel.active,  ##
        # WebhookConversationModel.local_created_at,  ##
        # WebhookConversationModel.local_updated_at,  ##
    ]

    # column_details_exclude_list = [  # If column_details_list not defined, all fields except defined
    #     WebhookConversationModel.local_created_at,
    #     WebhookConversationModel.local_updated_at, ]

    form_columns = [  # Edit form fields, all fields if not defined
        WebhookConversationModel.local_id,
        WebhookConversationModel.chats_subject_id,
        WebhookConversationModel.this_conversation_subject,
        WebhookConversationModel.event,  ##
        WebhookConversationModel.type,  ##
        WebhookConversationModel.id,  ##
        WebhookConversationModel.company_id,
        WebhookConversationModel.sender_name,
        WebhookConversationModel.sender_phone,
        WebhookConversationModel.sender_external_id,  ##
        WebhookConversationModel.sender_external_public_id,
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,  ##
        WebhookConversationModel.last_message_id,  ##
        WebhookConversationModel.operational_state,  ##
        WebhookConversationModel.replied_state,  ##
        WebhookConversationModel.group,
        WebhookConversationModel.created_at,  ##
        WebhookConversationModel.last_updated_at,  ##
        WebhookConversationModel.active,  ##
        # WebhookConversationModel.local_created_at,  ##
        # WebhookConversationModel.local_updated_at,  ##
    ]

    # form_excluded_columns = [  # If form_columns not defined
    #     "id",
    #     "created_at",
    #     "updated_at",
    #     "creation_reason", ]

    form_include_pk = True  # Display primary key fields in edit form or not

    form_overrides = {
        # See all possible fields types in:
        # from wtforms.fields.choices
        # from wtforms.fields.core
        # from wtforms.fields.datetime
        # from wtforms.fields.form
        # from wtforms.fields.list
        # from wtforms.fields.numeric
        # from wtforms.fields.simple
        # from wtforms.utils import unset_value,
        # "chats_subject_id": SelectMultipleField,
        # "this_conversation_subject": QuerySelectField,
    }

    form_widget_args = {  # Edit form fields additional properties
        # "local_id": {"readonly": True, "disabled": True},
        "chats_subject_id": {"disabled": True},
        # "this_conversation_subject": {"disabled": True},
        "event": {"disabled": True},
        "type": {"disabled": True},
        "id": {"disabled": True},
        "company_id": {"disabled": True},
        "sender_name": {"disabled": True},
        "sender_phone": {"disabled": True},
        "sender_external_id": {"disabled": True},
        "sender_external_public_id": {"disabled": True},
        "provider": {"disabled": True},
        "avatar_url": {"disabled": True},
        "last_message_id": {"disabled": True},
        "operational_state": {"disabled": True},
        "replied_state": {"disabled": True},
        "group": {"disabled": True},
        "created_at": {"disabled": True},
        "last_updated_at": {"disabled": True},
        # "active": {"disabled": True},
        "local_created_at": {"disabled": True},
        "local_updated_at": {"disabled": True}, }

    async def update_model(self, request: Request, pk: str, data: dict) -> None:
        # Preserve changing local_id via request or via editable form field
        # Some other functionality can be defined here on update
        data_with_old_pk = await self.set_new_data_old_pk_mixin(  # mixin func set_new_data_old_pkey_util() can be used
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
            "replied": PACT_LABELS.REPLIED_FILTER_LABEL,
            "unreplied": PACT_LABELS.UNREPLIED_FILTER_LABEL}
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
    def format_chats_subject_id_field(model_obj, attribute):
        parent_model_obj = getattr(model_obj, "this_conversation_subject")
        if parent_model_obj and parent_model_obj.chats_subject_name:
            display_value = parent_model_obj.chats_subject_name
            return display_value
        return ""

    @staticmethod
    # used by column_formatters/column_formatters_detail bellow, single field operation
    # model_obj = cur record, attribute = field string name
    def format_this_convers_subj_field(model_obj, attribute):
        parent_model_obj = getattr(model_obj, attribute)
        if parent_model_obj and parent_model_obj.chats_subject_name:
            if PACT_SQLADMIN_OPTIONS.DISPLAY_SUBJECT_AS_ARROW:
                return "<=="
            display_value = parent_model_obj.chats_subject_name
            return display_value
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
        WebhookConversationModel.replied_state: format_replied_state_field,
        WebhookConversationModel.chats_subject_id: format_chats_subject_id_field,
        WebhookConversationModel.this_conversation_subject: format_this_convers_subj_field,
        WebhookConversationModel.created_at: format_datetime_fields,
        WebhookConversationModel.last_updated_at: format_datetime_fields,
        WebhookConversationModel.local_created_at: format_datetime_fields,
        WebhookConversationModel.local_updated_at: format_datetime_fields,
        # WebhookConversationModel.current_status: format_created_at,  # as example for single field
        # WebhookConversationModel.current_status: format_current_status,  # as example for enum field
    }

    column_formatters_detail = {}
    column_formatters_detail.update(column_formatters)

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
