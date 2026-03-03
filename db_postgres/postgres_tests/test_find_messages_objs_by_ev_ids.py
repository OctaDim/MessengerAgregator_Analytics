if __name__ == "__main__":
    from db_postgres.postgres_queries.qry_get_message_obj_by_ev_id import (
        find_msg_obj_by_ev_id_qry)
    import asyncio
    from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
    from db_postgres.postgres_conn.postgres_session import PgsAsyncSession

    message_id = 425785
    # message_id = []
    # message_id = None

    async def test_find_messages_objs_by_ev_ids_qry():
        pgs_async_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_async_conn.engine,
                                   log_good_ops=True,
                                   ) as pgs_async_session:
            result = await find_msg_obj_by_ev_id_qry(
                ongoing_session=pgs_async_session,
                message_ev_id=message_id)
            return result


    print(asyncio.run(test_find_messages_objs_by_ev_ids_qry(), debug=True))
