from copy import copy
from typing import Any, Callable, List, Tuple, Union, Optional

from sqladmin._types import MODEL_ATTR
from sqladmin.filters import (
    BooleanFilter, StaticValuesFilter, ForeignKeyFilter)
from sqlalchemy import Select, or_
from starlette.requests import Request

from configs.labels_messages import LABELS
from configs.settings import SQLADMIN_FILTERS


# Defines possible human labels for boolean field filter
class CustomBooleanFilter(BooleanFilter):
    async def lookups(self, request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        custom_list = [
            ("all", LABELS.ALL_RECS_FILTER_LABEL),
            ("true", LABELS.YES_FILTER_LABEL),
            ("false", LABELS.NO_FILTER_LABEL), ]
        return custom_list


# Defines possible human labels for string field filter (as example)
class CustomRepliedStateFilter(StaticValuesFilter):
    async def lookups(self, request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        custom_list = [
            ("", LABELS.ALL_RECS_FILTER_LABEL),
            ("replied", LABELS.REPLIED_FILTER_LABEL),
            ("unreplied", LABELS.UNREPLIED_FILTER_LABEL), ]
        return custom_list


# Defines possible labels from field values plus "all" label for filter
class CustomStaticValuesFilter(StaticValuesFilter):
    async def lookups(self, request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        return [("", LABELS.ALL_RECS_FILTER_LABEL)] + self.values


# Defines possible labels for foreign key values plus substituted "all" label for filter
class CustomForeignKeyFilter(ForeignKeyFilter):
    async def lookups(self, request: Request, model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        parent_model_lookup = await super().lookups(request, model, run_query)
        substituted_lookup = copy(parent_model_lookup)
        substituted_lookup[0] = ("", LABELS.ALL_RECS_FILTER_LABEL)
        return substituted_lookup


class CustomAttachmentTypeFilter(StaticValuesFilter):
    def __init__(self,
                 column: Union[MODEL_ATTR, property],
                 values: List[Tuple[str, str]],
                 title: Optional[str] = None,
                 parameter_name: Optional[str] = None):
        super().__init__(column, values, title, parameter_name)

    async def lookups(self, request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        custom_list = [("all", LABELS.ALL_RECS_FILTER_LABEL),
                       ("audio", LABELS.AUDIO_FILE_FILTER_LABEL),
                       ("video", LABELS.VIDEO_FILE_FILTER_LABEL),
                       ("image", LABELS.IMAGE_FILE_FILTER_LABEL), ]
        return custom_list

    async def get_filtered_query(self, query: Select, value: Any, model: Any) -> Select:
        attachment_types = {
            "audio": (SQLADMIN_FILTERS.AUDIO_FILTER_EXTENSIONS,  # ext
                      SQLADMIN_FILTERS.AUDIO_FILTER_MIME_TYPES),  # mime
            "video": (SQLADMIN_FILTERS.VIDEO_FILTER_EXTENSIONS,
                      SQLADMIN_FILTERS.VIDEO_FILTER_MIME_TYPES),
            "image": (SQLADMIN_FILTERS.IMAGE_FILTER_EXTENSIONS,
                      SQLADMIN_FILTERS.IMAGE_FILTER_MIME_TYPES), }

        attachment_filters = attachment_types.get(value)
        if attachment_filters:
            extensions_list = attachment_filters[0]  # ext
            mime_types_list = attachment_filters[1]  # mime

            extension_conditions = []
            for cur_ext in extensions_list:
                cur_condition_query = model.file_name.ilike(f"%.{cur_ext}")
                extension_conditions.append(cur_condition_query)
            mime_conditions = []

            for cur_mime in mime_types_list:
                cur_condition_query = model.mime_type.ilike(f"%{cur_mime}%")
                mime_conditions.append(cur_condition_query)

            modified_query = query.filter(
                or_(*extension_conditions, *mime_conditions))
            return modified_query

            # # TODO: make filtering by hybrid properties
            # extension_conditions = []
            # for cur_ext in extensions_list:
            #     cur_condition_query = model.file_name.ilike(f"%.{cur_ext}")
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ cur_condition_query: ", cur_condition_query)
            #     extension_conditions.append(cur_condition_query)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ extension_conditions: ", extension_conditions)
            # mime_conditions = []
            # for cur_mime in mime_types_list:
            #     cur_condition_query = model.file_mime_type.ilike(f"%{cur_mime}%")
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ cur_condition_query: ", cur_condition_query)
            #     mime_conditions.append(cur_condition_query)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ mime_conditions: ", mime_conditions)
            #
            # modified_query = query.filter(
            #     or_(*extension_conditions, *mime_conditions))
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ modified_query: ", modified_query)
            # return modified_query
        else:
            return query

# class CustomCurrentStatusFilter(StaticValuesFilter):
#     async def lookups(
#             self, request: Request, model: Any,
#             run_query: Callable[[Select], Any]
#     ) -> List[Tuple[str, str]]:
#         custom_list = [("all", LABELS.ALL_RECS),
#                        ("new_category", LABELS.NEW_CLASS_ONLY),
#                        ("new_text", LABELS.NEW_TEXT_ONLY),
#                        ("new_category_text", LABELS.NEW_CLASS_AND_TEXT), ]
#         return custom_list
#
#     async def get_filtered_query(self, query: Select, value: Any, model: Any) -> Select:
#         new_cat_status = DRAFT_STATUS.NEW_CLASS_DRAFT_ADDED
#         new_text_status = DRAFT_STATUS.NEW_TEXT_DRAFT_ADDED
#         if value == "new_category":
#             return query.filter(
#                 DraftCategoryTextModel.current_status == new_cat_status)
#         elif value == "new_text":
#             return query.filter(
#                 DraftCategoryTextModel.current_status == new_text_status)
#         elif value == "new_category_text":
#             return query.filter(
#                 DraftCategoryTextModel.current_status.in_([
#                     new_cat_status, new_text_status]))
#         else:
#             return query

# class CustAccountDataFilter(StaticValuesFilter):
#     def __init__(self, column: Union[MODEL_ATTR, property],
#                  values: List[Tuple[str, str]],
#                  title: Optional[str] = None,
#                  parameter_name: Optional[str] = None):
#         super().__init__(column, values, title, parameter_name)
#
#     async def lookups(self, request: Request, model: Any,
#                       run_query: Callable[[Select], Any]
#                       ) -> List[Tuple[str, str]]:
#         return [("", LABELS.ALL_RECS)] + self.values

#     async def get_filtered_query(self, query: Select, value: Any, model: Any) -> Select:
#         if value == "":
#             return query
#         account_username = str(value).split("/")[0].strip()
#         account_id = str(value).split("/")[1].strip()
#         return query.filter(
#             DraftCategoryTextModel.account_username == account_username,
#             DraftCategoryTextModel.account_id == account_id)

# class CustomNewCategoryTextFilter(StaticValuesFilter):
#     async def lookups(
#             self, request: Request, model: Any,
#             run_query: Callable[[Select], Any]
#     ) -> List[Tuple[str, str]]:
#         custom_list = [("all", LABELS.ALL_RECS),
#                        ("new_category", LABELS.NEW_CLASS_ONLY),
#                        ("new_text", LABELS.NEW_TEXT_ONLY),
#                        ("new_category_text", LABELS.NEW_CLASS_AND_TEXT), ]
#         return custom_list

#     async def get_filtered_query(self, query: Select, value: Any, model: Any) -> Select:
#         new_item_mark = NEW_STATUS.NEW_RECORD
#         if value == "new_category":
#             return query.filter(
#                 DraftCategoryTextModel.new_category == new_item_mark,
#                 DraftCategoryTextModel.new_text != new_item_mark)
#         elif value == "new_text":
#             return query.filter(
#                 DraftCategoryTextModel.new_text == new_item_mark,
#                 DraftCategoryTextModel.new_category != new_item_mark)
#         elif value == "new_category_text":
#             return query.filter(
#                 DraftCategoryTextModel.new_category == new_item_mark,
#                 DraftCategoryTextModel.new_text == new_item_mark)
#         else:
#             return query
