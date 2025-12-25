from datetime import datetime

from sqladmin import ModelView
from starlette.requests import Request

from admin_panel.admin_views.mixin_set_new_data_old_pk import (
    OldPrimKeyNewDataMixin)
from admin_panel.custom_actions_mixins.mix_cancel_all_filters import (
    CanceAllFiltersSortsMixin)
from admin_panel.custom_classes.custom_filter_classes import (
    CustomBooleanFilter)
from configs.labels_messages import LABELS
from configs.settings import SQLADMIN_OPTIONS
from db_postgres.postgres_models.keywords_plus_model import (
    PlusKeywordsModel)


class PlusKeywordsAdmin(ModelView,
                        CanceAllFiltersSortsMixin,
                        OldPrimKeyNewDataMixin,  # Update mixin
                        model=PlusKeywordsModel):
    name = LABELS.PLUS_KEYWORD_PANEL_TITLE
    name_plural = LABELS.PLUS_KEYWORDS_PANEL_TITLE
    icon = LABELS.ICON
    category = LABELS.PLUS_KEYWORDS_CATEGORY_TITLE
    category_icon = LABELS.PLUS_KEYWORDS_CATEGORY_ICON
    is_async = True  # Default False
    page_size = 100
    page_size_options = [25, 50, 100, 200, 500, 1000]
    can_create = True  # Some bug: if not displayed or hidden, change can_export to False, restart, then True, restart
    can_delete = True
    can_edit = True
    can_view_details = True
    can_export = True

    column_list = [  # Main table columns
        PlusKeywordsModel.id,
        # PlusKeywordsModel.plus_subject_id,
        PlusKeywordsModel.plus_keyword,
        PlusKeywordsModel.active,
        PlusKeywordsModel.local_created_at,
        PlusKeywordsModel.local_updated_at,
    ]

    column_labels = {  # Human labels instead of table fields names
        PlusKeywordsModel.id: LABELS.ID_NUMBER,
        PlusKeywordsModel.plus_subject_id: LABELS.PLUS_KEYWORD,
        PlusKeywordsModel.plus_keyword: LABELS.PLUS_KEYWORD,
        PlusKeywordsModel.active: LABELS.ACTIVE,
        PlusKeywordsModel.local_created_at: LABELS.LOCAL_CREATED,
        PlusKeywordsModel.local_updated_at: LABELS.LOCAL_UPDATED,
    }

    column_searchable_list = [  # Search included fields
        PlusKeywordsModel.id,
        # PlusKeywordsModel.plus_subject_id,
        PlusKeywordsModel.plus_keyword,
        PlusKeywordsModel.active,
        PlusKeywordsModel.local_created_at,
        PlusKeywordsModel.local_updated_at,
    ]

    @property
    def column_filters(self):  # Standard and custom filters to filter column list
        column_filters_list = [
            # Filter using custom overridden filter class for boolean field
            CustomBooleanFilter(  # field: WebhookMessageModel.group
                column=PlusKeywordsModel.active,
                title=LABELS.ACTIVE_FILTER_TITLE),
        ]  # <== Do not remove or comment!!! It's used!!!
        return column_filters_list

    column_default_sort = [
        # (PlusKeywordsModel.plus_subject_id, False),  # True - descending, False - ascending
        (PlusKeywordsModel.plus_keyword, False),  # True - descending, False - ascending
        (PlusKeywordsModel.active, False),  # True - descending, False - ascending
    ]

    column_sortable_list = [  # Column list (main table) sortable fields
        PlusKeywordsModel.id,
        # PlusKeywordsModel.plus_subject_id,
        PlusKeywordsModel.plus_keyword,
        PlusKeywordsModel.active,
        PlusKeywordsModel.local_created_at,
        PlusKeywordsModel.local_updated_at,
    ]

    column_details_list = [  # Display form fields, all fields if not defined
        PlusKeywordsModel.id,
        # PlusKeywordsModel.plus_subject_id,
        PlusKeywordsModel.plus_keyword,
        PlusKeywordsModel.active,
        PlusKeywordsModel.local_created_at,
        PlusKeywordsModel.local_updated_at,
    ]

    # column_details_exclude_list = [  # If column_details_list not defined, all fields except defined
    #     PlusKeywordsModel.local_created_at,
    #     PlusKeywordsModel.local_updated_at, ]

    form_columns = [  # Edit form fields, all fields if not defined
        PlusKeywordsModel.id,
        # PlusKeywordsModel.plus_subject_id,
        PlusKeywordsModel.plus_keyword,
        PlusKeywordsModel.active,
        PlusKeywordsModel.local_created_at,
        PlusKeywordsModel.local_updated_at,
    ]

    # form_excluded_columns = [  # If form_columns not defined
    #     "id",
    #     "created_at",
    #     "updated_at", ]

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
        "plus_subject_id": {"readonly": True},
        "plus_keyword": {},
        "active": {},
        "local_created_at": {"readonly": False, "disabled": True},
        "local_updated_at": {"readonly": False, "disabled": True},
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
    def format_plus_keyword_field(model_obj, attribute):
        field_value = getattr(model_obj, attribute)
        if field_value and isinstance(field_value, str):
            truncation_limit = SQLADMIN_OPTIONS.PLUS_MINUS_WORDS_TRUNCATE_LIMIT
            if len(field_value) > truncation_limit:
                display_value = f"{field_value[:truncation_limit]}..."
            else:
                display_value = field_value
            return display_value
        elif not field_value:
            return ""
        else:
            return field_value

    column_formatters = {
        PlusKeywordsModel.local_created_at: format_datetime_fields,
        PlusKeywordsModel.local_updated_at: format_datetime_fields,
        PlusKeywordsModel.plus_keyword: format_plus_keyword_field,
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
