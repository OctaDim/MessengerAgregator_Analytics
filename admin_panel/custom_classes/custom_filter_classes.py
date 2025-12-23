from copy import copy
from typing import Any, Callable, List, Tuple, Union, Optional, Type

from sqladmin.filters import (
    BooleanFilter, StaticValuesFilter, ForeignKeyFilter)
from sqlalchemy import Select, or_, cast, String
from sqlalchemy.orm import InstrumentedAttribute, DeclarativeBase
from starlette.requests import Request

from configs.filters import SQLADMIN_FILTERS
from configs.labels_messages import LABELS
from db_postgres.postgres_init.declarative_base_model import Base


def get_column_obj(column: InstrumentedAttribute | str,
                   model: DeclarativeBase | Type[Base] = None
                   ) -> InstrumentedAttribute:
    if isinstance(column, str):
        if model is None:
            raise ValueError("model is required for string column filters")
        column_obj = getattr(model, column)
        return column_obj
    return column


# Defines possible human labels for boolean field filter
class CustomBooleanFilter(BooleanFilter):
    async def lookups(self,
                      request: Request,
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
    async def lookups(self,
                      request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        custom_list = [
            ("", LABELS.ALL_RECS_FILTER_LABEL),
            ("replied", LABELS.REPLIED_FILTER_LABEL),
            ("unreplied", LABELS.UNREPLIED_FILTER_LABEL), ]
        return custom_list


# Defines possible labels from field values plus "all" label for filter
class CustomStaticStringsFilter(StaticValuesFilter):
    async def lookups(self,
                      request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        return [("", LABELS.ALL_RECS_FILTER_LABEL)] + self.values


# IMPORTANT: value parameter returns str, so custom filter needed to filter numbers
# to convert value str to int explicitly and comparing with column field value
# Use for filtering int DB fields
# Defines possible labels from field values plus "all" label for filter
class CustomStaticNumbersFilter(StaticValuesFilter):
    async def lookups(self,
                      request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        return [("", LABELS.ALL_RECS_FILTER_LABEL)] + self.values

    async def get_filtered_query(self,
                                 query: Select,
                                 value: Any,
                                 model: Any) -> Select:
        if value:
            # column_obj = get_column_obj(self.column, model)
            return query.filter(cast(self.column, String) == value)  # Value returns str despite tuple values (int, int)
        else:
            return query


# Defines possible labels for foreign key values plus substituted "all" label for filter
class CustomForeignKeyFilter(ForeignKeyFilter):
    async def lookups(self,
                      request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        parent_lookup = await super().lookups(request, model, run_query)
        substituted_lookup = copy(parent_lookup)
        substituted_lookup[0] = ("", LABELS.ALL_RECS_FILTER_LABEL)
        return substituted_lookup


class CustomInviteUrlsFilter(StaticValuesFilter):
    def __init__(self,
                 column: Union[InstrumentedAttribute, str, property],
                 values: List[Tuple[str, str]],
                 title: Optional[str] = None,
                 parameter_name: Optional[str] = None):
        super().__init__(column, values, title, parameter_name)

    async def lookups(self, request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        custom_list = [("all", LABELS.ALL_RECS_FILTER_LABEL),
                       ("invites", LABELS.INVITES_FILTER_LABEL),
                       ("telegram", LABELS.TELEGRAM_FILTER_LABEL),
                       ("whatsapp", LABELS.WHATSAPP_FILTER_LABEL),
                       # ("discord", LABELS.DISCORD_FILTER_LABEL),
                       # ("slack", LABELS.SLACK_FILTER_LABEL),
                       # ("signal", LABELS.SIGNAL_FILTER_LABEL),
                       ("viber", LABELS.VIBER_FILTER_LABEL),
                       ("vk", LABELS.VK_FILTER_LABEL),
                       ("max", LABELS.MAX_FILTER_LABEL), ]
        return custom_list

    async def get_filtered_query(self, query: Select, value: Any, model: Any) -> Select:
        telegram_invites_urls = SQLADMIN_FILTERS.TELEGRAM_INVITES_URLS
        whatsapp_invites_urls = SQLADMIN_FILTERS.WHATSAPP_INVITES_URLS
        discord_invites_urls = SQLADMIN_FILTERS.DISCORD_INVITES_URLS
        viber_invites_urls = SQLADMIN_FILTERS.VIBER_INVITES_URLS
        slack_invites_urls = SQLADMIN_FILTERS.SLACK_INVITES_URLS
        signal_invites_urls = SQLADMIN_FILTERS.SIGNAL_INVITES_URLS
        vk_invites_urls = SQLADMIN_FILTERS.VK_INVITES_URLS
        max_invites_urls = SQLADMIN_FILTERS.MAX_INVITES_URLS
        all_invites_urls = (
                telegram_invites_urls + whatsapp_invites_urls +
                discord_invites_urls + viber_invites_urls +
                slack_invites_urls + signal_invites_urls +
                vk_invites_urls + max_invites_urls)

        invites_urls_types = {
            "telegram": telegram_invites_urls,  # urls
            "whatsapp": whatsapp_invites_urls,
            "discord": discord_invites_urls,
            "viber": viber_invites_urls,
            "slack": slack_invites_urls,
            "signal": signal_invites_urls,
            "vk": vk_invites_urls,
            "max": max_invites_urls,
            "invites": all_invites_urls, }

        invites_urls_list = invites_urls_types.get(value)
        if invites_urls_list:
            invites_urls_conditions = []
            for cur_invite_url in invites_urls_list:
                cur_invite_query = model.message.ilike(f"%{cur_invite_url}%")  # Contains <cur_invite_url>
                invites_urls_conditions.append(cur_invite_query)
            modified_query = query.filter(or_(*invites_urls_conditions))
            return modified_query
        else:
            return query


class CustomAttachedMediaTypeFilter(StaticValuesFilter):
    def __init__(self,
                 column: Union[InstrumentedAttribute, str, property],
                 values: List[Tuple[str, str]],
                 title: Optional[str] = None,
                 parameter_name: Optional[str] = None):
        super().__init__(column, values, title, parameter_name)

    async def lookups(self, request: Request,
                      model: Any,
                      run_query: Callable[[Select], Any]
                      ) -> List[Tuple[str, str]]:
        custom_list = [("all", LABELS.ALL_RECS_FILTER_LABEL),
                       ("all_media", LABELS.MEDIA_FILE_FILTER_LABEL),
                       ("audio", LABELS.AUDIO_FILE_FILTER_LABEL),
                       ("video", LABELS.VIDEO_FILE_FILTER_LABEL),
                       ("image", LABELS.IMAGE_FILE_FILTER_LABEL),
                       ("docs", LABELS.DOCS_FILE_FILTER_LABEL), ]
        return custom_list

    async def get_filtered_query(self, query: Select, value: Any, model: Any) -> Select:
        audio_extensions = SQLADMIN_FILTERS.AUDIO_FILTER_EXTENSIONS
        audio_mime_types = SQLADMIN_FILTERS.AUDIO_FILTER_MIME_TYPES

        video_extensions = SQLADMIN_FILTERS.VIDEO_FILTER_EXTENSIONS
        video_mime_types = SQLADMIN_FILTERS.VIDEO_FILTER_MIME_TYPES

        image_extensions = SQLADMIN_FILTERS.IMAGE_FILTER_EXTENSIONS
        image_mime_types = SQLADMIN_FILTERS.IMAGE_FILTER_MIME_TYPES

        docs_extensions = SQLADMIN_FILTERS.DOCS_FILTER_EXTENSIONS
        docs_mime_types = SQLADMIN_FILTERS.DOCS_FILTER_MIME_TYPES

        attachment_types = {
            "audio": (audio_extensions, audio_mime_types),  # (ext, mime)
            "video": (video_extensions, video_mime_types),
            "image": (image_extensions, image_mime_types),
            "docs": (docs_extensions, docs_mime_types),
            "media": (audio_extensions + video_extensions + image_extensions,
                      audio_mime_types + video_mime_types + image_mime_types), }

        attachment_filters = attachment_types.get(value)
        if attachment_filters:
            extensions_list = attachment_filters[0]  # ext
            mime_types_list = attachment_filters[1]  # mime

            extension_conditions = []
            for cur_ext in extensions_list:
                # TODO: make filtering by hybrid properties pty_file_name
                cur_condition_query = model.file_name.ilike(f"%.{cur_ext}")  # Ends with ".<cur_ext>"
                extension_conditions.append(cur_condition_query)
            mime_conditions = []

            for cur_mime in mime_types_list:
                # TODO: make filtering by hybrid properties pty_mime_type
                cur_condition_query = model.mime_type.ilike(f"%{cur_mime}%")  # Contains <cur_mime>
                mime_conditions.append(cur_condition_query)

            united_conditions = extension_conditions + mime_conditions  # United filters
            modified_query = query.filter(or_(*united_conditions))
            return modified_query
        else:
            return query

# TODO: Settle a question of not displaying provider
# # Defines possible unique labels for foreign key values plus substituted "all" label for filter
# class CustomUniqueProviderForeignKeyFilter(ForeignKeyFilter):
#     async def lookups(self,
#                       request: Request, model: Any,
#                       run_query: Callable[[Select], Any]
#                       ) -> List[Tuple[str, str]]:
#         parent_lookup = await super().lookups(request, model, run_query)
#         filters_dict = {}
#         for filter_key, filter_label in parent_lookup[1:]:
#             cur_label_keys = filters_dict.get(filter_label, [])
#             cur_label_keys.append(filter_key)
#             filters_dict[filter_label] = cur_label_keys
#
#         modified_lookup = [("", LABELS.ALL_RECS_FILTER_LABEL)]
#         for cur_label, cur_keys in filters_dict.items():
#             new_filter_entry = (",".join(cur_keys), cur_label)
#             modified_lookup.append(new_filter_entry)
#         print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ modified_lookup: {modified_lookup}")
#         return modified_lookup
#
#     async def get_filtered_query(self,
#                                  query: Select,
#                                  value: Any,
#                                  model: Any) -> Select:
#         value_str_list = value.split(",")  # str to list, because value is str like "21,34,11"
#         print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ value_str_list: {value_str_list}")
#         print(f"QQQQQQQQQQQQQQQQQQQQQQQ value_str_list[0]: {value_str_list[0]}")
#         print("QQQQQQQQQQQQQQQQQQQQQQQ type(value_str_list[0]): ", type(value_str_list[0]))
#
#         value_int_list = [int(cur_str_id) for cur_str_id in value_str_list]
#         print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ value_int_list: {value_int_list}")
#         print(f"QQQQQQQQQQQQQQQQQQQQQQQ value_int_list[0]: {value_int_list[0]}")
#         print("QQQQQQQQQQQQQQQQQQQQQQQ type(value_int_list[0]): ", type(value_int_list[0]))
#
#         # foreign_key_obj = get_column_obj(self.foreign_key, model)
#         # print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ self.foreign_key: {self.foreign_key}")
#         # print(f"QQQQQQQQQQQQQQQQQQQQQQQ model: {model}")
#         # print(f"QQQQQQQQQQQQQQQQQQQQQQQ foreign_key_obj: {foreign_key_obj}")
#         # column_type = foreign_key_obj.type
#         # value = value_str_list[0]
#         # if isinstance(column_type, (Integer, Numeric, Float, BigInteger, SmallInteger,)):
#         #     print("1111111111111111111111111111111111111111111111111111111111")
#         #     value = int(value)
#         print("1111111111111111111111111111111111111111111111111111111")
#         # value_int_list = [7]
#         if value_int_list:
#             print("22222222222222222222222222222222222222222222222222222222")
#             modified_query = query.where(WebhookMessageModel.conversation_local_id.in_(value_int_list))
#             print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ value_int_list: {value_int_list}")
#             print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ modified_query: {modified_query}")
#
#             pgs_conn = PgsAsyncConnection()
#             async with (PgsAsyncSession(engine=pgs_conn.engine,
#                                         log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS
#                                         ) as pgs_session):
#                 modified_qry_res = await pgs_session.execute(modified_query)
#                 print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ modified_qry_res: {modified_qry_res.scalars().all()}")
#             return modified_query
#         else:
#             print("333333333333333333333333333333333333333333333333333")
#             pgs_conn = PgsAsyncConnection()
#             async with (PgsAsyncSession(engine=pgs_conn.engine,
#                                         log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_SESSION_OK_ACTIONS_LOGS
#                                         ) as pgs_session):
#                 qry_res = await pgs_session.execute(query)
#                 print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ qry_res: {qry_res.scalars().all()}")
#             return query

# TODO: Settle a question of not displaying foreign records
# # Defines possible unique labels for foreign key values plus substituted "all" label for filter
# class CustomUniqueForeignKeyFilter(ForeignKeyFilter):
#     async def lookups(self,
#                       request: Request, model: Any,
#                       run_query: Callable[[Select], Any]
#                       ) -> List[Tuple[str, str]]:
#         parent_lookup = await super().lookups(request, model, run_query)
#         filters_dict = {}
#         for filter_key, filter_label in parent_lookup[1:]:
#             cur_label_keys = filters_dict.get(filter_label, [])
#             cur_label_keys.append(filter_key)
#             filters_dict[filter_label] = cur_label_keys
#
#         modified_lookup = [("", LABELS.ALL_RECS_FILTER_LABEL)]
#         for cur_label, cur_keys in filters_dict.items():
#             new_filter_entry = (",".join(cur_keys), cur_label)
#             modified_lookup.append(new_filter_entry)
#         print(f"\nQQQQQQQQQQQQQQQQQQQQQQQ modified_lookup: {modified_lookup}")
#         print(f"QQQQQQQQQQQQQQQQQQQQQQQ type(modified_lookup): {type(modified_lookup)}")
#         return modified_lookup
#
#     async def get_filtered_query(self, query: Select, value: Any, model: Any) -> Select:
#         value_str_list = value.split(",")  # str to list, because value is always str
#         print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ value_str_list: {value_str_list}")
#         print(f"QQQQQQQQQQQQQQQQQQQQQQQ value_str_list[0]: {value_str_list[0]}")
#         print("QQQQQQQQQQQQQQQQQQQQQQQ type(value_str_list[0]): ", type(value_str_list[0]))
#
#         value_int_list = [int(cur_str_id) for cur_str_id in value_str_list]
#         print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ value_int_list: {value_int_list}")
#         print(f"QQQQQQQQQQQQQQQQQQQQQQQ value_int_list[0]: {value_int_list[0]}")
#         print("QQQQQQQQQQQQQQQQQQQQQQQ type(value_int_list[0]): ", type(value_int_list[0]))
#
#         foreign_key_obj = get_column_obj(self.foreign_key, model)
#         print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ self.foreign_key: {self.foreign_key}")
#         print(f"QQQQQQQQQQQQQQQQQQQQQQQ model: {model}")
#         print(f"QQQQQQQQQQQQQQQQQQQQQQQ foreign_key_obj: {foreign_key_obj}")
#         query = query.filter(foreign_key_obj.in_([19,]))
#         # query = query.filter(foreign_key_obj.in_([39, 37]))
#         # query = query.filter(cast(foreign_key_obj, String).in_(value_str_list))
#         # query = query.filter(cast(foreign_key_obj, String).in_(value_str_list))
#         # query = query.filter(cast(foreign_key_obj, String).in_(value_int_list))
#         # query = query.filter(foreign_key_obj.in_(value_int_list))
#         print(f"\n\nQQQQQQQQQQQQQQQQQQQQQQQ query: {query}")
#         return query

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
