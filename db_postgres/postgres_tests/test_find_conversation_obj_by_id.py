if __name__ == "__main__":
    import asyncio
    from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
    from db_postgres.postgres_conn.postgres_session import PgsAsyncSession
    from db_postgres.postgres_queries._pact_pgs_queries.qry_find_conversation_obj_by_id import (
        find_convers_obj_by_id_qry)

    company_id = 100179
    conversation_id = 219052713


    async def test_find_conversation_data_by_id():
        pgs_async_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_async_conn.engine,
                                   log_good_ops=True,
                                   ) as pgs_async_session:
            result = await find_convers_obj_by_id_qry(
                ongoing_session=pgs_async_session,
                company_id=company_id,
                conversation_id=conversation_id)
            return result


    print(asyncio.run(test_find_conversation_data_by_id(), debug=True))
