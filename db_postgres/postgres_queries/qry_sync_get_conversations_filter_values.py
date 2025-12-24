from typing import Dict, List, Tuple

from configs.settings import ALCHEMY_OPTIONS
from db_postgres.postgres_conn.pgs_connection import (
    PgsSyncConnection)
from db_postgres.postgres_conn.postgres_session import (
    PgsSyncSession)
from db_postgres.postgres_models.webhook_conversation_model import (
    WebhookConversationModel)
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_sync_model_rows_flex_query)


def get_sync_conversation_filters_values_qry() -> Dict[str, List[Tuple[any, any]]]:
    pgs_sync_conn = PgsSyncConnection()
    with PgsSyncSession(engine=pgs_sync_conn.engine,
                        log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
                        ) as pgs_sync_session:
        selected_fields = ["provider",
                           "company_id", ]

        pgs_conversation_objs = get_sync_model_rows_flex_query(
            orm_model_class=WebhookConversationModel,
            ongoing_session=pgs_sync_session,
            selected_fields=selected_fields,
            fields_values_filter=None,
            order_by_fields=None,
            return_scalars=False)

        provider_set = set()
        company_id_set = set()
        for cur_convers in pgs_conversation_objs:
            cur_provider = cur_convers.provider
            cur_company_id = cur_convers.company_id
            # cur_acc_data = f"{cur_username} / {cur_acc_id}"  # Just as example

            provider_set.add(cur_provider) if cur_provider else None
            company_id_set.add(cur_company_id) if cur_company_id else None

        provider_set = sorted(provider_set)
        company_id_set = sorted(company_id_set)

        filter_provider_values = [(cat, cat) for cat in provider_set]
        filter_company_id_values = [(txt, txt) for txt in company_id_set]

        conversation_filter_data = {
            "provider_values": filter_provider_values,
            "company_id_values": filter_company_id_values, }
        return conversation_filter_data
