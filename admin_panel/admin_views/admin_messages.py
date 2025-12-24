from datetime import datetime

from sqladmin import ModelView
from starlette.requests import Request

from admin_panel.admin_views.mixin_update_model_old_pk_val import (
    set_old_pkey_in_new_data_mixin)
from admin_panel.custom_actions_mixins.mix_cancel_all_filters import (
    CanceAllFiltersSortsMixin)
from admin_panel.custom_classes.custom_filter_classes import (
    CustomBooleanFilter, CustomAttachedMediaTypeFilter,
    CustomStaticNumbersFilter, CustomInviteUrlsFilter)
from configs.labels_messages import LABELS
from configs.settings import SQLADMIN_OPTIONS
from db_postgres.postgres_models.webhook_message_model import (
    WebhookMessageModel)
from db_postgres.postgres_queries.qry_sync_get_messages_filter_values import (
    get_sync_message_filters_values_qry)


class MessagesAdmin(ModelView,
                    CanceAllFiltersSortsMixin,
                    model=WebhookMessageModel):
    name = LABELS.MESSAGE_PANEL_TITLE
    name_plural = LABELS.MESSAGES_PANEL_TITLE
    icon = LABELS.ICON
    category = LABELS.MESSAGES_CATEGORY_TITLE
    category_icon = LABELS.MESSAGES_CATEGORY_ICON
    is_async = True  # Default False
    page_size = 200
    page_size_options = [25, 50, 100, 200, 500, 1000]
    can_create = False  # Some bug: if not displayed or hidden, change can_export to False, restart, then True, restart
    can_delete = False
    can_edit = False
    can_view_details = True
    can_export = True

    column_list = [  # Main table columns
        WebhookMessageModel.local_id,
        WebhookMessageModel.conversation_local_id,
        WebhookMessageModel.event,
        WebhookMessageModel.type,  ##
        WebhookMessageModel.id,  ##
        WebhookMessageModel.provider,
        WebhookMessageModel.sender_name,
        # WebhookMessageModel.emoji_count,
        # WebhookMessageModel.webp_count,
        # WebhookMessageModel.external_id,  ##
        WebhookMessageModel.company_id,
        WebhookMessageModel.conversation_id,  ##
        # WebhookMessageModel.contact_id,
        WebhookMessageModel.replied_to_id,  ##
        WebhookMessageModel.income,
        WebhookMessageModel.status,  ##
        # WebhookMessageModel.reactions,  ##
        WebhookMessageModel.details,  ##
        WebhookMessageModel.file_name,
        # WebhookMessageModel.pty_file_name,  # property
        # WebhookMessageModel.mime_type,
        # WebhookMessageModel.pty_mime_type,  # property
        WebhookMessageModel.push_to_talk,
        # WebhookMessageModel.pty_push_to_talk,  # property
        WebhookMessageModel.message,
        # WebhookMessageModel.attachment_url,
        # WebhookMessageModel.pty_attachment_url,  # property
        # WebhookMessageModel.attachments,  ##
        WebhookMessageModel.created_at,
        # WebhookMessageModel.external_created_at,
        # WebhookMessageModel.local_created_at,
        # WebhookMessageModel.local_updated_at,
    ]

    column_labels = {  # Human labels instead of table fields names
        WebhookMessageModel.local_id: LABELS.LOCAL_ID,
        WebhookMessageModel.conversation_local_id: LABELS.CONVERSATION_LOCAL_ID,
        WebhookMessageModel.event: LABELS.EVENT,
        WebhookMessageModel.type: LABELS.TYPE,
        WebhookMessageModel.id: LABELS.ID,
        WebhookMessageModel.provider: LABELS.PROVIDER,
        WebhookMessageModel.sender_name: LABELS.SENDER_NAME,
        WebhookMessageModel.emoji_count: LABELS.EMOJI_COUNT,
        WebhookMessageModel.webp_count: LABELS.WEBP_COUNT,
        WebhookMessageModel.external_id: LABELS.EXTERNAL_ID,
        WebhookMessageModel.company_id: LABELS.COMPANY_ID,
        WebhookMessageModel.conversation_id: LABELS.CONVERSATION_ID,
        WebhookMessageModel.contact_id: LABELS.CONTACT_ID,
        WebhookMessageModel.replied_to_id: LABELS.REPLIED_TO_ID,
        WebhookMessageModel.income: LABELS.INCOME,
        WebhookMessageModel.status: LABELS.STATUS,
        WebhookMessageModel.message: LABELS.MESSAGE,
        WebhookMessageModel.reactions: LABELS.REACTIONS,
        WebhookMessageModel.details: LABELS.DETAILS,
        WebhookMessageModel.attachments: LABELS.ATTACHMENTS,
        WebhookMessageModel.attachment_url: LABELS.ATTACHMENT_URL,
        WebhookMessageModel.file_name: LABELS.FILE_NAME,
        WebhookMessageModel.mime_type: LABELS.MIME_TYPE,
        WebhookMessageModel.push_to_talk: LABELS.PUSH_TO_TALK,
        WebhookMessageModel.created_at: LABELS.CREATED_AT,
        WebhookMessageModel.external_created_at: LABELS.UPDATED_AT,
        WebhookMessageModel.local_created_at: LABELS.LOCAL_CREATED,
        WebhookMessageModel.local_updated_at: LABELS.LOCAL_UPDATED,
        WebhookMessageModel.delivery: LABELS.DELIVERY,
        WebhookMessageModel.deleted: LABELS.DELETED,
        WebhookMessageModel.active: LABELS.ACTIVE,
    }

    column_searchable_list = [  # Search included fields
        WebhookMessageModel.local_id,
        WebhookMessageModel.conversation_local_id,
        WebhookMessageModel.event,
        WebhookMessageModel.type,  ##
        WebhookMessageModel.id,  ##
        WebhookMessageModel.provider,
        WebhookMessageModel.sender_name,
        # WebhookMessageModel.emoji_count,
        # WebhookMessageModel.webp_count,
        WebhookMessageModel.external_id,  ##
        WebhookMessageModel.company_id,
        WebhookMessageModel.conversation_id,  ##
        WebhookMessageModel.contact_id,
        WebhookMessageModel.replied_to_id,  ##
        WebhookMessageModel.income,
        WebhookMessageModel.status,  ##
        # WebhookMessageModel.reactions,  ##
        WebhookMessageModel.details,  ##
        WebhookMessageModel.file_name,
        # WebhookMessageModel.pty_file_name,  # property
        WebhookMessageModel.mime_type,
        # WebhookMessageModel.pty_mime_type,  # property
        WebhookMessageModel.push_to_talk,
        # WebhookMessageModel.pty_push_to_talk,  # property
        WebhookMessageModel.message,
        # WebhookMessageModel.attachment_url,
        # WebhookMessageModel.pty_attachment_url,  # property
        # WebhookMessageModel.attachments,  ##
        WebhookMessageModel.created_at,
        # WebhookMessageModel.external_created_at,
        # WebhookMessageModel.local_created_at,
        # WebhookMessageModel.local_updated_at,
    ]

    @property
    def column_filters(self):  # Standard and custom filters to filter column list
        filters_values = get_sync_message_filters_values_qry()  # All possible unique and sorted values for filters
        convers_local_id_keys = filters_values["convers_local_id_keys"]
        company_id_keys = filters_values["company_id_keys"]
        provider_keys = filters_values["provider_keys"]
        sender_name_keys = filters_values["sender_name_keys"]

        column_filters_list = [
            # Filter using custom overridden filter class for boolean field
            CustomBooleanFilter(  # field: WebhookMessageModel.group
                column=WebhookMessageModel.income,
                title=LABELS.INCOME_FILTER_TITLE),

            CustomStaticNumbersFilter(  # field: WebhookMessageModel.company_id
                # Filter using custom overridden filter class for int(number) field
                column=WebhookMessageModel.company_id,
                values=company_id_keys,
                title=LABELS.COMPANY_ID_FILTER_TITLE),

            CustomAttachedMediaTypeFilter(  # combined fields: WebhookMessageModel.file_name and mime_type
                # Filter using custom overridden filter class for string field
                column=WebhookMessageModel.mime_type,  # Used by parent to define Model class, but not in overridden
                values=[],  # Defined in overridden CustomRepliedStateFilter (def lookups), but can be defined here
                title=LABELS.FILE_TYPE_FILTER_TITLE),

            CustomBooleanFilter(  # field: WebhookMessageModel.push_to_talk
                # Filter using custom overridden filter class for boolean field
                column=WebhookMessageModel.push_to_talk,
                title=LABELS.VOICE_MESSAGE_FILTER_TITLE),

            # TODO: Settle a question of not displaying provider
            # CustomUniqueProviderForeig1nKeyFilter(  # foreign key field: customer_id (display field: account_id)
            #     foreign_key=WebhookMessageModel.conversation_local_id,
            #     foreign_display_field=WebhookConversationModel.provider,
            #     foreign_model=WebhookConversationModel,
            #     title=LABELS.PROVIDER),

            CustomStaticNumbersFilter(  # field: WebhookMessageModel.conversation_local_id
                # Filter using custom overridden filter class for int(number) field
                column=WebhookMessageModel.provider,
                values=provider_keys,
                title=LABELS.PROVIDER_FILTER_TITLE),

            CustomInviteUrlsFilter(  # field: WebhookMessageModel.conversation_local_id
                # Filter using custom overridden filter class for int(number) field
                column=WebhookMessageModel.message,
                values=[],
                title=LABELS.INVITES_FILTER_TITLE),

            CustomStaticNumbersFilter(  # field: WebhookMessageModel.conversation_local_id
                # Filter using custom overridden filter class for int(number) field
                column=WebhookMessageModel.sender_name,
                values=sender_name_keys,
                title=LABELS.SENDER_NAME_FILTER_TITLE),

            # CustomStaticNumbersFilter(  # field: WebhookMessageModel.conversation_local_id
            #     # Filter using custom overridden filter class for int(number) field
            #     column=WebhookMessageModel.conversation_local_id,
            #     values=convers_local_id_keys,
            #     title=LABELS.CONVERS_LOCAL_ID_FILTER_TITLE),

            # CustomRepliedStateFilter(  # field: WebhookMessageModel.replied_state
            # # Filter using custom overridden filter class for string field
            #     column=WebhookMessageModel.replied_state,
            #     values=[],  # Defined in overridden CustomRepliedStateFilter and 'def lookups', can be defined here
            #     title=LABELS.REPLIED_FILTER_TITLE),

            # Filter using custom overridden filter class for property model field
            # CustAccountDataFilter(  # combine fields: account_username, account_id
            #     column=WebhookMessageModel.account_data,
            #     values=acc_data_values,
            #     title=LABELS.FILTER_ACCOUNT_DATA),

            # CustomNewCategoryTextFilter(  # combine fields: new_category, new_text
            #     column=WebhookMessageModel.new_category,
            #     values=[("all", LABELS.ALL_RECS),
            #             ("new_category", LABELS.NEW_CLASS_ONLY),
            #             ("new_text", LABELS.NEW_TEXT_ONLY),
            #             ("new_category_text", LABELS.NEW_CLASS_AND_TEXT)],
            #     title=LABELS.FILTER_NEW_DRAFT),

            # CustomStaticValuesFilter(  # field: account_username
            #     column=WebhookMessageModel.account_username,
            #     values=username_values,
            #     title=LABELS.FILTER_ACCOUNT_USERNAME),

            # CustomStaticValuesFilter(  # field: account_id
            #     column=WebhookMessageModel.account_id,
            #     values=acc_id_values,
            #     title=LABELS.ACCOUNT_ID),

            # CustomForeignKeyFilter(  # foreign key field: customer_id (display field: account_id)
            #     foreign_key=WebhookMessageModel.conversation_local_id,
            #     foreign_display_field=WebhookConversationModel.provider,
            #     foreign_model=WebhookConversationModel,
            #     title=LABELS.PROVIDER),

            # CustomForeignKeyFilter(  # foreign key field: customer_id (display field: account_id)
            #     foreign_key=WebhookMessageModel.customer_id,
            #     foreign_display_field=CustomerModel.account_id,
            #     foreign_model=CustomerModel,
            #     title=LABELS.FILTER_ACCOUNT_ID),

        ]  # <== Do not remove or comment!!! It's used!!!
        return column_filters_list

    column_default_sort = [
        (WebhookMessageModel.local_id, True),  # True - descending, False - ascending
        (WebhookMessageModel.active, False),  # True - descending, False - ascending
    ]

    column_sortable_list = [  # Column list (main table) sortable fields
        WebhookMessageModel.local_id,
        WebhookMessageModel.conversation_local_id,
        WebhookMessageModel.event,
        WebhookMessageModel.type,
        WebhookMessageModel.id,
        WebhookMessageModel.provider,
        WebhookMessageModel.sender_name,
        WebhookMessageModel.emoji_count,
        WebhookMessageModel.webp_count,
        WebhookMessageModel.external_id,
        WebhookMessageModel.company_id,
        WebhookMessageModel.conversation_id,
        WebhookMessageModel.contact_id,
        WebhookMessageModel.replied_to_id,
        WebhookMessageModel.income,
        WebhookMessageModel.status,
        WebhookMessageModel.message,
        WebhookMessageModel.reactions,
        WebhookMessageModel.details,
        WebhookMessageModel.attachments,
        WebhookMessageModel.attachment_url,
        WebhookMessageModel.file_name,
        WebhookMessageModel.mime_type,
        WebhookMessageModel.push_to_talk,
        # WebhookMessageModel.pty_file_name,
        # WebhookMessageModel.pty_mime_type,
        WebhookMessageModel.created_at,
        WebhookMessageModel.external_created_at,
        WebhookMessageModel.local_created_at,
        WebhookMessageModel.local_updated_at,
    ]

    column_details_list = [  # Display form fields, all fields if not defined
        WebhookMessageModel.local_id,
        WebhookMessageModel.conversation_local_id,
        WebhookMessageModel.event,
        WebhookMessageModel.type,  ##
        WebhookMessageModel.id,  ##
        WebhookMessageModel.provider,
        WebhookMessageModel.sender_name,
        # WebhookMessageModel.emoji_count,
        # WebhookMessageModel.webp_count,
        # WebhookMessageModel.external_id,  ##
        WebhookMessageModel.company_id,
        WebhookMessageModel.conversation_id,  ##
        # WebhookMessageModel.contact_id,
        WebhookMessageModel.replied_to_id,  ##
        WebhookMessageModel.income,
        WebhookMessageModel.status,  ##
        # WebhookMessageModel.reactions,  ##
        WebhookMessageModel.details,  ##
        WebhookMessageModel.file_name,
        # WebhookMessageModel.pty_file_name,  # property
        # WebhookMessageModel.mime_type,
        # WebhookMessageModel.pty_mime_type,  # property
        WebhookMessageModel.push_to_talk,
        # WebhookMessageModel.pty_push_to_talk,  # property
        WebhookMessageModel.message,
        # WebhookMessageModel.attachment_url,
        # WebhookMessageModel.pty_attachment_url,  # property
        # WebhookMessageModel.attachments,  ##
        WebhookMessageModel.created_at,
        WebhookMessageModel.external_created_at,
        # WebhookMessageModel.local_created_at,
        # WebhookMessageModel.local_updated_at,
    ]

    # column_details_exclude_list = [  # If column_details_list not defined, all fields except defined
    #     WebhookMessageModel.local_created_at,
    #     WebhookMessageModel.local_updated_at, ]

    form_columns = [  # Edit form fields, all fields if not defined
        WebhookMessageModel.local_id,
        WebhookMessageModel.conversation_local_id,
        WebhookMessageModel.event,
        WebhookMessageModel.type,  ##
        WebhookMessageModel.id,  ##
        WebhookMessageModel.provider,
        WebhookMessageModel.sender_name,
        # WebhookMessageModel.emoji_count,
        # WebhookMessageModel.webp_count,
        # WebhookMessageModel.external_id,  ##
        WebhookMessageModel.company_id,
        WebhookMessageModel.conversation_id,  ##
        # WebhookMessageModel.contact_id,
        WebhookMessageModel.replied_to_id,  ##
        WebhookMessageModel.income,
        WebhookMessageModel.status,  ##
        # WebhookMessageModel.reactions,  ##
        WebhookMessageModel.details,  ##
        WebhookMessageModel.file_name,
        # WebhookMessageModel.pty_file_name,  # property
        # WebhookMessageModel.mime_type,
        # WebhookMessageModel.pty_mime_type,  # property
        WebhookMessageModel.push_to_talk,
        # WebhookMessageModel.pty_push_to_talk,  # property
        WebhookMessageModel.message,
        # WebhookMessageModel.attachment_url,
        # WebhookMessageModel.pty_attachment_url,  # property
        # WebhookMessageModel.attachments,  ##
        WebhookMessageModel.created_at,
        # WebhookMessageModel.external_created_at,
        # WebhookMessageModel.local_created_at,
        # WebhookMessageModel.local_updated_at,
    ]

    # form_excluded_columns = [  # If form_columns not defined
    #     "id",
    #     "created_at",
    #     "updated_at",
    #     "creation_reason", ]

    form_include_pk = False  # Display primary key fields in edit form or not

    # Preserve changing local_id via request or via editable form field
    # Some other functionality can be defined on update
    async def update_model(self, request: Request, pk: str, data: dict) -> None:
        data_with_old_pk = await set_old_pkey_in_new_data_mixin(
            orm_model=self.model,
            prim_key_value_str=pk,
            prim_key_name="local_id",
            form_data=data)
        return await super().update_model(request, pk, data=data_with_old_pk)

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
    def format_sender_name_field(model_obj, attribute):
        field_value = getattr(model_obj, attribute)
        if field_value and isinstance(field_value, str):
            truncation_limit = SQLADMIN_OPTIONS.SENDER_NAME_FILTER_TRUNC_LIMIT
            if len(field_value) > truncation_limit:
                display_value = f"{field_value[:truncation_limit]}..."
            else:
                display_value = field_value
            return display_value
        elif not field_value:
            return ""
        else:
            return field_value

    @staticmethod
    # used by column_formatters/column_formatters_detail bellow, single field operation
    # model_obj = cur record, attribute = field string name
    def format_message_field(model_obj, attribute):
        field_value = getattr(model_obj, attribute)
        if field_value and isinstance(field_value, str):
            truncation_limit = SQLADMIN_OPTIONS.MESSAGE_SYMBOLS_TRUNCATE_LIMIT
            if len(field_value) > truncation_limit:
                display_value = f"{field_value[:truncation_limit]}..."
            else:
                display_value = field_value
            return display_value
        elif not field_value:
            return ""
        else:
            return field_value

    @staticmethod
    # used by column_formatters/column_formatters_detail bellow, single field operation
    # model_obj = cur record, attribute = field string name
    def format_reactions_field(model_obj, attribute):
        field_value = getattr(model_obj, attribute)
        if field_value and isinstance(field_value, list):
            display_value = "+".join(field_value)
            return display_value
        elif not field_value:
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
        WebhookMessageModel.created_at: format_datetime_fields,
        WebhookMessageModel.external_created_at: format_datetime_fields,
        WebhookMessageModel.local_created_at: format_datetime_fields,
        WebhookMessageModel.local_updated_at: format_datetime_fields,
        WebhookMessageModel.message: format_message_field,
        WebhookMessageModel.sender_name: format_sender_name_field,
        WebhookMessageModel.reactions: format_reactions_field,
        # WebhookMessageModel.current_status: format_created_at,  # as example for single field
        # WebhookMessageModel.current_status: format_current_status,  # as example for enum field
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
