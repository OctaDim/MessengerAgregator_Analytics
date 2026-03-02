from db_postgres.postgres_queries.qry_get_messages_list_by_ev_ids import (
    find_messages_objs_by_ev_ids_qry)

if __name__ == "__main__":
    import asyncio
    from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
    from db_postgres.postgres_conn.postgres_session import PgsAsyncSession

    # messages_ids = [425785]
    messages_ids = [425785, 425670, 7818]
    # messages_ids = []
    # messages_ids = None

    async def test_find_messages_objs_by_ev_ids_qry():
        pgs_async_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_async_conn.engine,
                                   log_good_ops=True,
                                   ) as pgs_async_session:
            result = await find_messages_objs_by_ev_ids_qry(
                ongoing_session=pgs_async_session,
                messages_ids=messages_ids)
            return result


    print(asyncio.run(test_find_messages_objs_by_ev_ids_qry(), debug=True))
