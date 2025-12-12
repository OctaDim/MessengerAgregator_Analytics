from datetime import datetime

from sqladmin import ModelView
from sqlalchemy import select
from starlette.requests import Request

from admin_panel.custom_actions_mixins.mix_cancel_all_filters import (
    CanceAllFiltersSortsMixin)
from admin_panel.custom_classes.custom_filter_classes import (
    CustomBooleanFilter, CustomRepliedStateFilter,
    CustomStaticValuesFilter)
from configs.labels_messages import LABELS
from configs.settings import ALCHEMY_OPTIONS
from db_postgres.postgres_conn.pgs_connection import (
    PgsSyncConnection, PgsAsyncConnection)
from db_postgres.postgres_conn.postgres_session import (
    PgsSyncSession, PgsAsyncSession)
from db_postgres.postgres_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_queries.qry_get_conversations_filter_values import (
    get_sync_convers_filters_values_qry)


class ConversationsAdmin(ModelView,
                         CanceAllFiltersSortsMixin,
                         model=WebhookConversationModel):
    name = LABELS.CONVERSATION
    name_plural = LABELS.CONVERSATIONS
    icon = LABELS.ICON
    # category = "SOME CATEGORY"
    # category_icon = "CATEGORY ICON"
    is_async = True  # Default False
    page_size = 200
    page_size_options = [25, 50, 100, 200]
    can_create = False  # Some bug: if not displayed or hidden, change can_export to False, restart, then True, restart
    can_delete = False
    can_edit = False
    can_view_details = True
    can_export = True

    column_list = [  # Main table columns
        WebhookConversationModel.local_id,
        # WebhookConversationModel.event,
        # WebhookConversationModel.type,
        # WebhookConversationModel.id,
        WebhookConversationModel.company_id,  #
        WebhookConversationModel.sender_name,  #
        WebhookConversationModel.sender_phone,  #
        # WebhookConversationModel.sender_external_id,
        WebhookConversationModel.sender_external_public_id,  #
        WebhookConversationModel.provider,
        # WebhookConversationModel.avatar_url,
        # WebhookConversationModel.last_message_id,
        # WebhookConversationModel.operational_state,
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
        WebhookConversationModel.event,
        WebhookConversationModel.type,
        WebhookConversationModel.id,
        WebhookConversationModel.company_id,
        WebhookConversationModel.sender_name,
        WebhookConversationModel.sender_phone,
        WebhookConversationModel.sender_external_id,
        WebhookConversationModel.sender_external_public_id,
        WebhookConversationModel.provider,
        WebhookConversationModel.avatar_url,
        WebhookConversationModel.last_message_id,
        WebhookConversationModel.operational_state,
        WebhookConversationModel.replied_state,
        WebhookConversationModel.group,
        WebhookConversationModel.created_at,
        WebhookConversationModel.last_updated_at,
        WebhookConversationModel.active,
        WebhookConversationModel.local_created_at,
        WebhookConversationModel.local_updated_at,
    ]

    @property
    def column_filters(self):  # Standard and custom filters to filter column list
        pgs_sync_conn = PgsSyncConnection()
        with PgsSyncSession(
                engine=pgs_sync_conn.engine,
                log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
        ) as pgs_sync_session:
            # Getting all possible unique and sorted values for filters
            filters_values = get_sync_convers_filters_values_qry(
                ongoing_sync_session=pgs_sync_session)
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
                CustomStaticValuesFilter(  # field: WebhookConversationModel.provider
                    column=WebhookConversationModel.provider,
                    values=providers_values,
                    title=LABELS.PROVIDER_FILTER_TITLE),

                # Filter using custom overridden filter class for string field
                CustomStaticValuesFilter(  # field: draft_category
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
        (WebhookConversationModel.active, True),  # True - ascending, False - descending
        (WebhookConversationModel.created_at, True),  # True - ascending, False - descending
    ]

    column_sortable_list = [  # Column list (main table) sortable fields
        WebhookConversationModel.local_id,
        WebhookConversationModel.event,
        WebhookConversationModel.type,
        WebhookConversationModel.id,
        WebhookConversationModel.company_id,
        WebhookConversationModel.sender_name,
        WebhookConversationModel.sender_phone,
        WebhookConversationModel.sender_external_id,
        WebhookConversationModel.sender_external_public_id,
        WebhookConversationModel.provider,
        WebhookConversationModel.avatar_url,
        WebhookConversationModel.last_message_id,
        WebhookConversationModel.operational_state,
        WebhookConversationModel.replied_state,
        WebhookConversationModel.group,
        WebhookConversationModel.created_at,
        WebhookConversationModel.last_updated_at,
        WebhookConversationModel.active,
        WebhookConversationModel.local_created_at,
        WebhookConversationModel.local_updated_at,
    ]

    # column_details_list = [  # Display form fields, all fields if not defined
    #     WebhookConversationModel.id,
    #     WebhookConversationModel.account_data,
    #     WebhookConversationModel.ds_existing_category,
    #     WebhookConversationModel.draft_category,
    #     WebhookConversationModel.ds_existing_text,
    #     WebhookConversationModel.draft_text,
    #     WebhookConversationModel.current_status,
    #     WebhookConversationModel.active,
    #     WebhookConversationModel.created_at, ]

    # column_details_exclude_list = [  # If column_details_list not defined, all fields except defined
    #     WebhookConversationModel.local_created_at,
    #     WebhookConversationModel.local_updated_at, ]

    # form_columns = [  #  Edit form fields, all fields if not defined
    #     WebhookConversationModel.account_id,
    #     WebhookConversationModel.account_username,
    #     WebhookConversationModel.ds_existing_category,
    #     WebhookConversationModel.draft_category,
    #     WebhookConversationModel.ds_existing_text,
    #     WebhookConversationModel.draft_text,
    #     WebhookConversationModel.current_status,
    #     WebhookConversationModel.active,
    #     WebhookConversationModel.created_at, ]

    # form_excluded_columns = [  # If form_columns not defined
    #     "id",
    #     "created_at",
    #     "updated_at",
    #     "creation_reason", ]

    form_include_pk = False  # Display primary key fields in edit form or not

    # Preserve changing field value via request or via editable form field, or some other logic on update
    async def update_model(self, request: Request, pk: str, data: dict) -> None:
        pgs_async_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_async_conn.engine,
                                   log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
                                   ) as pgs_async_session:
            on_update_query = select(self.model).where(self.model.local_id == int(pk))
            query_result = await pgs_async_session.execute(on_update_query)
            current_obj = query_result.scalar_one()
            data["local_id"] = current_obj.local_id
            return await super().update_model(request, pk, data)

    # form_widget_args = {  # Edit form fields additional properties
    #     "local_id": {"readonly": True, "disabled": True},
    #     "created_at": {"readonly": True},
    #     "last_updated_at": {"readonly": True},
    #     "local_created_at": {"readonly": True},
    #     "local_updated_at": {"readonly": True}, }

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
        field_value_label = replied_states_labels.get(field_value)
        if field_value_label:
            return field_value_label
        elif not field_value_label:
            return ""
        else:
            return field_value

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
