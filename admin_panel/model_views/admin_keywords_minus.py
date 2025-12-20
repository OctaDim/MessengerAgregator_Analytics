from datetime import datetime

from sqladmin import ModelView
from sqlalchemy import select
from starlette.requests import Request

from admin_panel.custom_actions_mixins.mix_cancel_all_filters import (
    CanceAllFiltersSortsMixin)
from admin_panel.custom_classes.custom_filter_classes import (
    CustomBooleanFilter)
from configs.labels_messages import LABELS
from configs.settings import ALCHEMY_OPTIONS, SQLADMIN_OPTIONS
from db_postgres.postgres_conn.pgs_connection import (
    PgsAsyncConnection)
from db_postgres.postgres_conn.postgres_session import (
    PgsAsyncSession)
from db_postgres.postgres_models.keywords_minus_model import (
    MinusKeywordsModel)


class MinusKeywordsAdmin(ModelView,
                        CanceAllFiltersSortsMixin,
                        model=MinusKeywordsModel):
    name = LABELS.MINUS_KEYWORD_PANEL_TITLE
    name_plural = LABELS.MINUS_KEYWORDS_PANEL_TITLE
    icon = LABELS.ICON
    category = LABELS.MINUS_KEYWORDS_CATEGORY_TITLE
    category_icon = LABELS.MINUS_KEYWORDS_CATEGORY_ICON
    is_async = True  # Default False
    page_size = 100
    page_size_options = [25, 50, 100, 200, 500, 1000]
    can_create = True  # Some bug: if not displayed or hidden, change can_export to False, restart, then True, restart
    can_delete = True
    can_edit = True
    can_view_details = True
    can_export = True

    column_list = [  # Main table columns
        MinusKeywordsModel.id,
        # MinusKeywordsModel.minus_subject_id,
        MinusKeywordsModel.minus_keyword,
        MinusKeywordsModel.active,
        MinusKeywordsModel.local_created_at,
        MinusKeywordsModel.local_updated_at,
    ]

    column_labels = {  # Human labels instead of table fields names
        MinusKeywordsModel.id: LABELS.ID_NUMBER,
        MinusKeywordsModel.minus_subject_id: LABELS.MINUS_SUBJECT,
        MinusKeywordsModel.minus_keyword: LABELS.MINUS_KEYWORD,
        MinusKeywordsModel.active: LABELS.ACTIVE,
        MinusKeywordsModel.local_created_at: LABELS.LOCAL_CREATED,
        MinusKeywordsModel.local_updated_at: LABELS.LOCAL_UPDATED,
    }

    column_searchable_list = [  # Search included fields
        MinusKeywordsModel.id,
        # MinusKeywordsModel.minus_subject_id,
        MinusKeywordsModel.minus_keyword,
        MinusKeywordsModel.active,
        MinusKeywordsModel.local_created_at,
        MinusKeywordsModel.local_updated_at,
    ]

    @property
    def column_filters(self):  # Standard and custom filters to filter column list
        column_filters_list = [
            # Filter using custom overridden filter class for boolean field
            CustomBooleanFilter(  # field: WebhookMessageModel.group
                column=MinusKeywordsModel.active,
                title=LABELS.ACTIVE_FILTER_TITLE),
        ]  # <== Do not remove or comment!!! It's used!!!
        return column_filters_list

    column_default_sort = [
        # (MinusKeywordsModel.minus_subject_id, False),  # True - descending, False - ascending
        (MinusKeywordsModel.minus_keyword, False),  # True - descending, False - ascending
        (MinusKeywordsModel.active, False),  # True - descending, False - ascending
    ]

    column_sortable_list = [  # Column list (main table) sortable fields
        MinusKeywordsModel.id,
        # MinusKeywordsModel.minus_subject_id,
        MinusKeywordsModel.minus_keyword,
        MinusKeywordsModel.active,
        MinusKeywordsModel.local_created_at,
        MinusKeywordsModel.local_updated_at,
    ]

    column_details_list = [  # Display form fields, all fields if not defined
        MinusKeywordsModel.id,
        # MinusKeywordsModel.minus_subject_id,
        MinusKeywordsModel.minus_keyword,
        MinusKeywordsModel.active,
        MinusKeywordsModel.local_created_at,
        MinusKeywordsModel.local_updated_at,
    ]

    # column_details_exclude_list = [  # If column_details_list not defined, all fields except defined
    #     MinusKeywordsModel.local_created_at,
    #     MinusKeywordsModel.local_updated_at, ]

    form_columns = [  # Edit form fields, all fields if not defined
        MinusKeywordsModel.id,
        # MinusKeywordsModel.minus_subject_id,
        MinusKeywordsModel.minus_keyword,
        MinusKeywordsModel.active,
        # MinusKeywordsModel.local_created_at,
        # MinusKeywordsModel.local_updated_at,
    ]

    # form_excluded_columns = [  # If form_columns not defined
    #     "id",
    #     "created_at",
    #     "updated_at", ]

    form_include_pk = False  # Display primary key fields in edit form or not

    # Preserve changing field value via request or via editable form field, or some other logic on update
    async def update_model(self, request: Request, pk: str, data: dict) -> None:
        pgs_async_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_async_conn.engine,
                                   log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
                                   ) as pgs_async_session:
            on_update_query = select(self.model).where(self.model.id == int(pk))
            query_result = await pgs_async_session.execute(on_update_query)
            current_obj = query_result.scalar_one()
            data["id"] = current_obj.id
            return await super().update_model(request, pk, data)

    form_widget_args = {  # Edit form fields additional properties
        "id": {"readonly": True, "disabled": True},
        "minus_subject_id": {"readonly": True},
        "minus_keyword": {},
        "active": {},
        "created_at": {"readonly": True, "disabled": True},
        "updated_at": {"readonly": True, "disabled": True},
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
    def format_minus_keyword_field(model_obj, attribute):
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
        MinusKeywordsModel.local_created_at: format_datetime_fields,
        MinusKeywordsModel.local_updated_at: format_datetime_fields,
        MinusKeywordsModel.minus_keyword: format_minus_keyword_field,
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
