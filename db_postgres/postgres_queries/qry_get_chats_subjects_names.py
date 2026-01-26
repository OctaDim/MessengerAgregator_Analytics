from sqlalchemy import select

from configs.settings import ALCHEMY_OPTIONS
from db_postgres.postgres_conn.pgs_connection import PgsAsyncConnection, PgsSyncConnection
from db_postgres.postgres_conn.postgres_session import PgsAsyncSession, PgsSyncSession
from db_postgres.postgres_models.chats_subjects_model import ChatsSubjectModel


async def get_chats_subjects_qry_async():
    pgs_async_conn = PgsAsyncConnection()
    async with PgsAsyncSession(engine=pgs_async_conn.engine,
                               log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
                               ) as pgs_async_session:
        query = select(ChatsSubjectModel).order_by(ChatsSubjectModel.chats_subject_name)
        result = await pgs_async_session.execute(query)
        subjects = result.scalars().all()
        return subjects


def get_chats_subjects_query_sync():
    pgs_sync_conn = PgsSyncConnection()
    with PgsSyncSession(engine=pgs_sync_conn.engine,
                        log_good_ops=ALCHEMY_OPTIONS.ALCHEMY_ORM_RAW_SQL_LOGS
                        ) as pgs_sync_session:
        query = select(ChatsSubjectModel).order_by(ChatsSubjectModel.chats_subject_name)
        result = pgs_sync_session.execute(query)
        subjects = result.scalars().all()
        return subjects
