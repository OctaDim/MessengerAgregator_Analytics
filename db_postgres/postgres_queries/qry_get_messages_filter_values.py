from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from db_postgres.postgres_models.webhook_message_model import WebhookMessageModel
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_sync_model_rows_flex_query)


def get_sync_msgs_filters_values_qry(
        ongoing_sync_session: Session
) -> Dict[str, List[Tuple[any, any]]]:
    selected_fields = ["conversation_local_id",
                       "company_id", ]

    pgs_message_objs = get_sync_model_rows_flex_query(
        orm_model_class=WebhookMessageModel,
        ongoing_session=ongoing_sync_session,
        selected_fields=selected_fields,
        fields_values_filter=None,
        order_by_fields=None,
        return_scalars=False)

    convers_local_id_set = set()
    company_id_set = set()
    for cur_message in pgs_message_objs:
        cur_convers_local_id = cur_message.conversation_local_id
        cur_company_id = cur_message.company_id
        # cur_acc_data = f"{cur_username} / {cur_acc_id}"  # Just as example

        convers_local_id_set.add(cur_convers_local_id) if cur_convers_local_id else None
        company_id_set.add(cur_company_id) if cur_company_id else None

    convers_local_id_set = sorted(convers_local_id_set)
    company_id_set = sorted(company_id_set)

    filter_convers_local_id_values = [(_id, _id) for _id in convers_local_id_set]
    filter_company_id_values = [(txt, txt) for txt in company_id_set]

    messages_filter_data = {
        "convers_local_id_values": filter_convers_local_id_values,
        "company_id_values": filter_company_id_values, }
    return messages_filter_data
