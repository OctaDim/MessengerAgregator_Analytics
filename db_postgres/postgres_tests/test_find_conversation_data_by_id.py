if __name__ == "__main__":
    import asyncio
    from db_postgres.postgres_queries.qry_find_conversation_data_by_id import (
        find_conversation_data_by_id)
    from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection
    from db_postgres.postgres_conn.postgres_session import PgsAsyncSession

    company_id = 100179
    conversation_id = 219052713


    async def test_find_conversation_data_by_id():
        pgs_async_conn = PgsAsyncConnection()
        async with PgsAsyncSession(engine=pgs_async_conn.engine) as pgs_async_session:
            result = await find_conversation_data_by_id(
                ongoing_session=pgs_async_session,
                company_id=company_id,
                conversation_id=conversation_id)
            return result

    print(asyncio.run(test_find_conversation_data_by_id(), debug=True))
