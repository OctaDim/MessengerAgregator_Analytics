import copy
from typing import Type

from sqlalchemy.orm import DeclarativeBase

from configs.settings import ALCHEMY_OPTIONS
from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
from db_postgres.postgres_conn.postgres_session import PgsAsyncSession
from db_postgres.postgres_init.declarative_base_model import Base
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_model_rows_flex_query)


async def set_old_pkey_in_new_data_mixin(
        orm_model: Type[Base] | Type[DeclarativeBase] | Type,
        prim_key_value_str: str,
        prim_key_name: str,
        form_data: dict
) -> dict[str, any]:
    pgs_async_conn = PgsAsyncConnection()
    async with PgsAsyncSession(engine=pgs_async_conn.engine,
                               log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
                               ) as pgs_async_session:
        model_objects = await get_model_rows_flex_query(
            orm_model_class=orm_model,
            ongoing_session=pgs_async_session,
            selected_fields=None,
            fields_values_filter={prim_key_name: int(prim_key_value_str)},
            order_by_fields=None,
            distinct_on=None,
            return_scalars=True)
    obj_before_update = model_objects[0]
    fixed_data = copy.deepcopy(form_data)
    for fld_name, fld_value in form_data.items():  # because not form modified fields are always None, old values used
        if fld_value is None and hasattr(obj_before_update, fld_name):
            fixed_data[fld_name] = getattr(obj_before_update, fld_name)
    fixed_data["local_id"] = obj_before_update.local_id
    return fixed_data
