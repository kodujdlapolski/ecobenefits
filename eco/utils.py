from contextlib import contextmanager

import aioredis
import redis
from sqlalchemy.engine.base import Engine
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
    return await aioredis.create_redis(
        (config.REDIS_HOST, config.REDIS_PORT),
        db=config.REDIS_DB,
    )


@contextmanager
def session_scope(engine: Engine) -> Session:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
