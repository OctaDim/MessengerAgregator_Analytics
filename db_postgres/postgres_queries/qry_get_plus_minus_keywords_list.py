from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from db_postgres.postgres_models.keywords_minus_model import (
    MinusKeywordsModel)
from db_postgres.postgres_models.keywords_plus_model import (
    PlusKeywordsModel)
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_model_rows_flex_query)


async def get_plus_keywords_list_qry(
        ongoing_sync_session: AsyncSession
) -> List[str]:
    selected_fields = ["plus_subject_id",
                       "plus_keyword", ]

    pgs_plus_keywords_objs = await get_model_rows_flex_query(
        orm_model_class=PlusKeywordsModel,
        ongoing_session=ongoing_sync_session,
        selected_fields=selected_fields,
        fields_values_filter=None,
        order_by_fields=None,
        return_scalars=False)

    plus_keywords_set = set()
    for cur_word_obj in pgs_plus_keywords_objs:
        plus_keywords_set.add(cur_word_obj.plus_keyword.lower())

    plus_keywords_list = list(plus_keywords_set)
    return plus_keywords_list


async def get_minus_keywords_list_qry(
        ongoing_sync_session: AsyncSession
) -> List[str]:
    selected_fields = ["minus_subject_id",
                       "minus_keyword", ]

    pgs_minus_keywords_objs = await get_model_rows_flex_query(
        orm_model_class=MinusKeywordsModel,
        ongoing_session=ongoing_sync_session,
        selected_fields=selected_fields,
        fields_values_filter=None,
        order_by_fields=None,
        return_scalars=False)

    minus_keywords_set = set()
    for cur_word_obj in pgs_minus_keywords_objs:
        minus_keywords_set.add(cur_word_obj.plus_keyword.lower())

    plus_keywords_list = list(minus_keywords_set)
    return plus_keywords_list
