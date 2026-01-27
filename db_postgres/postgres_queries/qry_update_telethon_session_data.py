from typing import Dict

from configs.settings import ALCHEMY_OPTIONS
from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
from db_postgres.postgres_conn.postgres_session import PgsAsyncSession
from db_postgres.postgres_models.telethon_configs_model import (
    TelethonConfigModel)
from db_postgres.postgres_queries_utils.update_existing_model_objects import (
    update_existing_model_objs_qry)


async def update_telethon_session_data_qry(
        telethon_config_id: int,
        web_account_id: str,
        web_account_username: str,
        update_data: Dict[str, str]
) -> bool:
    pgs_conn = PgsAsyncConnection()
    async with PgsAsyncSession(engine=pgs_conn.engine,
                               log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
                               ) as pgs_sync_session:
        filter_fields = {"id": telethon_config_id,
                         "web_account_id": web_account_id,
                         "web_account_username": web_account_username}

        await update_existing_model_objs_qry(
            ModelClassORM=TelethonConfigModel,
            ongoing_session=pgs_sync_session,
            fields_values_filter=filter_fields,
            update_data=update_data)

        return None
