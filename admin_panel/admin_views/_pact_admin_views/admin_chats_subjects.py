from datetime import datetime

from sqladmin import ModelView
from starlette.requests import Request

from admin_panel.admin_views.mixin_set_new_data_old_pk import (
    OldPrimKeyNewDataMixin)
from admin_panel.custom_actions_mixins._pact_custom_actions.mix_cancel_all_filters import (
    CanceAllFiltersSortsMixin)
from admin_panel.custom_classes._pact_custom_classes.custom_filter_classes import (
    CustomBooleanFilter)
from configs.labels_messages import PACT_LABELS
from configs.settings import PACT_SQLADMIN_OPTIONS
from db_postgres.postgres_models._pact_pgs_models.chats_subjects_model import (
    ChatsSubjectModel)


class ChatSubjectsAdmin(ModelView,
                        CanceAllFiltersSortsMixin,
                        OldPrimKeyNewDataMixin,  # Update mixin
                        model=ChatsSubjectModel):
    name = PACT_LABELS.CHAT_SUBJECT_PANEL_TITLE
    name_plural = PACT_LABELS.CHAT_SUBJECTS_PANEL_TITLE
    icon = PACT_LABELS.ICON
    category = PACT_LABELS.CHAT_SUBJECTS_CATEGORY_TITLE
    category_icon = PACT_LABELS.CHAT_SUBJECTS_CATEGORY_ICON
    is_async = True  # Default False
    page_size = 100
    page_size_options = [25, 50, 100, 200, 500, 1000]
    can_create = True  # Some bug: if not displayed or hidden, change can_export to False, restart, then True, restart
    can_delete = True
    can_edit = True
    can_view_details = True
    can_export = True

    column_list = [  # Main table columns
        ChatsSubjectModel.id,
        ChatsSubjectModel.chats_subject_name,
        ChatsSubjectModel.this_subject_conversations,
        ChatsSubjectModel.active,
        ChatsSubjectModel.local_created_at,
        ChatsSubjectModel.local_updated_at,
    ]

    column_labels = {  # Human labels instead of table fields names
        ChatsSubjectModel.id: PACT_LABELS.ID_NUMBER,
        ChatsSubjectModel.chats_subject_name: PACT_LABELS.CHATS_SUBJECT,
        ChatsSubjectModel.this_subject_conversations: PACT_LABELS.SUBJECT_CHATS,
    ChatsSubjectModel.active: PACT_LABELS.ACTIVE,
        ChatsSubjectModel.local_created_at: PACT_LABELS.LOCAL_CREATED,
        ChatsSubjectModel.local_updated_at: PACT_LABELS.LOCAL_UPDATED,
    }

    column_searchable_list = [  # Search included fields
        ChatsSubjectModel.id,
        ChatsSubjectModel.chats_subject_name,
        ChatsSubjectModel.this_subject_conversations,
        ChatsSubjectModel.active,
        ChatsSubjectModel.local_created_at,
        ChatsSubjectModel.local_updated_at,
    ]

    @property
    def column_filters(self):  # Standard and custom filters to filter column list
        column_filters_list = [
            # Filter using custom overridden filter class for boolean field
            CustomBooleanFilter(  # field: ChatsSubjectModel.active
                column=ChatsSubjectModel.active,
                title=PACT_LABELS.ACTIVE_FILTER_TITLE),
        ]  # <== Do not remove or comment!!! It's used!!!
        return column_filters_list

    column_default_sort = [
        # (MinusKeywordsModel.minus_subject_id, False),  # True - descending, False - ascending
        (ChatsSubjectModel.chats_subject_name, False),  # True - descending, False - ascending
        (ChatsSubjectModel.active, False),  # True - descending, False - ascending
    ]

    column_sortable_list = [  # Column list (main table) sortable fields
        ChatsSubjectModel.id,
        ChatsSubjectModel.chats_subject_name,
        # ChatsSubjectModel.this_subject_conversations,
        ChatsSubjectModel.active,
        ChatsSubjectModel.local_created_at,
        ChatsSubjectModel.local_updated_at,
    ]

    column_details_list = [  # Display form fields, all fields if not defined
        ChatsSubjectModel.id,
        ChatsSubjectModel.chats_subject_name,
        ChatsSubjectModel.this_subject_conversations,
        ChatsSubjectModel.active,
        ChatsSubjectModel.local_created_at,
        ChatsSubjectModel.local_updated_at,
    ]

    # column_details_exclude_list = [  # If column_details_list not defined, all fields except defined
    #     ChatsSubjectModel.local_created_at,
    #     ChatsSubjectModel.local_updated_at, ]

    form_columns = [  # Edit form fields, all fields if not defined
        ChatsSubjectModel.id,
        ChatsSubjectModel.chats_subject_name,
        ChatsSubjectModel.this_subject_conversations,
        ChatsSubjectModel.active,
        ChatsSubjectModel.local_created_at,
        ChatsSubjectModel.local_updated_at,
    ]

    # form_excluded_columns = [  # If form_columns not defined
    #     "id",
    #     "local_created_at",
    #     "local_updated_at", ]

    form_include_pk = False  # Display primary key fields in edit form or not

    async def update_model(self, request: Request, pk: str, data: dict) -> None:
        # Preserve changing local_id via request or via editable form field
        # Some other functionality can be defined here on update
        data_with_old_pk = await self.set_new_data_old_pk_mixin(  # mixin func set_new_data_old_pkey_util() can be used
            prim_key_value_str=pk,
            prim_key_name="id",
            form_data=data)
        return await super().update_model(request, pk, data=data_with_old_pk)

    form_widget_args = {  # Edit form fields additional properties
        "id": {"readonly": True, "disabled": True},
        "chats_subject_name": {},
        "active": {},
        "local_created_at": {"readonly": True, "disabled": True},
        "local_updated_at": {"readonly": True, "disabled": True},
    }

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
    def format_chats_subject_field(model_obj, attribute):
        field_value = getattr(model_obj, attribute)
        if field_value and isinstance(field_value, str):
            truncation_limit = PACT_SQLADMIN_OPTIONS.CHATS_SUBJECT_TRUNCATE_LIMIT
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
    def format_this_subj_convers_field(model_obj, attribute):
        nested_model_objs = getattr(model_obj, attribute)
        if nested_model_objs:
            subject_chats_set = set()
            for cur_nested_obj in nested_model_objs:
                if cur_nested_obj.sender_name:
                    subject_chats_set.add(cur_nested_obj.sender_name)
                    # sorted(subject_chats_set)
            return subject_chats_set
        return ""

    column_formatters = {
        ChatsSubjectModel.this_subject_conversations: format_this_subj_convers_field,
        ChatsSubjectModel.local_created_at: format_datetime_fields,
        ChatsSubjectModel.local_updated_at: format_datetime_fields,
        ChatsSubjectModel.chats_subject_name: format_chats_subject_field,
    }

    column_formatters_detail = {
        ChatsSubjectModel.this_subject_conversations: format_this_subj_convers_field,
        ChatsSubjectModel.local_created_at: format_datetime_fields,
        ChatsSubjectModel.local_updated_at: format_datetime_fields,
        ChatsSubjectModel.chats_subject_name: format_chats_subject_field,
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
