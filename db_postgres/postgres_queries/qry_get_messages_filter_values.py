from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from configs.settings import SQLADMIN_OPTIONS
from db_postgres.postgres_models.webhook_message_model import WebhookMessageModel
from db_postgres.postgres_queries_utils.get_model_records_flex_query import (
    get_sync_model_rows_flex_query)


def get_sync_filters_keys_labels_qry(
        ongoing_sync_session: Session
) -> Dict[str, List[Tuple[any, any]]]:
    selected_fields = ["conversation_local_id",
                       "company_id",
                       "provider",
                       "sender_name", ]

    pgs_message_objs = get_sync_model_rows_flex_query(
        orm_model_class=WebhookMessageModel,
        ongoing_session=ongoing_sync_session,
        selected_fields=selected_fields,
        fields_values_filter=None,
        order_by_fields=None,
        return_scalars=False)

    convers_local_id_set = set()
    company_id_set = set()
    provider_set = set()
    sender_name_set = set()
    for cur_message in pgs_message_objs:
        cur_convers_local_id = cur_message.conversation_local_id
        cur_company_id = cur_message.company_id
        cur_provider = cur_message.provider
        cur_sender_name = cur_message.sender_name
        # cur_acc_data = f"{cur_username} / {cur_acc_id}"  # Just as example

        convers_local_id_set.add(cur_convers_local_id) if cur_convers_local_id else None
        company_id_set.add(cur_company_id) if cur_company_id else None
        provider_set.add(cur_provider) if cur_provider else None
        sender_name_set.add(cur_sender_name) if cur_sender_name else None

    convers_local_id_set = sorted(convers_local_id_set)
    company_id_set = sorted(company_id_set)
    provider_set = sorted(provider_set)
    sender_name_set = sorted(sender_name_set)

    filter_convers_local_id_keys = [(_id, _id) for _id in convers_local_id_set]
    filter_company_id_keys = [(_id, _id) for _id in company_id_set]
    filter_provider_keys = [(prov, prov) for prov in provider_set]

    filter_sender_name_keys = []
    for cur_sender_name in sender_name_set:
        sender_name_limit = SQLADMIN_OPTIONS.SENDER_NAME_FILTER_TRUNC_LIMIT
        if len(cur_sender_name) > sender_name_limit:
            truncated_sender_name = f"{cur_sender_name[:sender_name_limit]}..."
            cur_sender_name_key = (cur_sender_name, truncated_sender_name)
        else:
            cur_sender_name_key = (cur_sender_name, cur_sender_name)
        filter_sender_name_keys.append(cur_sender_name_key)

    filter_keys_data = {
        "convers_local_id_keys": filter_convers_local_id_keys,
        "company_id_keys": filter_company_id_keys,
        "provider_keys": filter_provider_keys,
        "sender_name_keys": filter_sender_name_keys, }
    return filter_keys_data
