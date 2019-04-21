from contextlib import contextmanager

import aioredis
import redis
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from eco import config


def get_sync_redis_conn() -> redis.Redis:
    return redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
    )


async def get_async_redis_conn() -> aioredis.RedisConnection:
    r = await aioredis.create_redis(
        (config.REDIS_HOST, config.REDIS_PORT),
        db=config.REDIS_DB,
    )
    return r


@contextmanager
def session_scope(engine) -> Session:
    """
    SQLite session manager.
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        # Should reraise the exception.
        raise
    finally:
        session.close()
