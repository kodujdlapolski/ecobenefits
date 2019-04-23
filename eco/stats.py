import logging
from typing import Any, Dict, Union

import aioredis
import redis
import ujson
from sqlalchemy import Column, Float, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

from eco import config
from eco.data_utils import load_models
from eco.eco_model import predict_tree_benefits
from eco.utils import session_scope

logger = logging.getLogger(__name__)

Base = declarative_base()  # type: Any
conn = f'postgresql+psycopg2://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}'
engine = create_engine(conn)
Base.metadata.bind = engine

# Warsaw in mapadrzew.pl
SOURCE_INSTANCE_ID = 1


class Tree(Base):
    __tablename__ = 'treemap_tree'
    id = Column(Integer, primary_key=True)
    instance_id = Column(Integer)
    diameter = Column(Float)


class OTMDatabaseBackend:
    """
    Open Tree Map database connector
    """

    def get_trees(self) -> list:
        with session_scope(engine) as session:
            trees = session.query(Tree).filter_by(instance_id=SOURCE_INSTANCE_ID).all()
            return [t.diameter for t in trees if t.diameter]


class EcoStatistics:
    stats_key = 'eco_stats'
    db_backend = OTMDatabaseBackend

    def __init__(self, redis_conn: Union[redis.Redis, aioredis.Redis]) -> None:
        self.redis_conn = redis_conn
        self.db = self.db_backend()
        self.eco_models = load_models(config.MODELS_PATH)

    def compute_stats(self) -> None:
        """
        Fetches all trees from the external database
        and stores total eco statistics in Redis.
        """
        logger.info('Fetching trees from the database')
        trees = self.db.get_trees()
        trees_count = len(trees)
        stats: Dict[str, Any] = {
            'benefits': {
                'NO2': 0.0,
                'O3': 0.0,
                'PM2.5': 0.0,
                'SO2': 0.0,
            },
            'trees_count': trees_count,
        }

        for diam in trees:
            benefits = predict_tree_benefits(self.eco_models, diam)
            for factor, value in benefits.items():
                stats_factor = stats['benefits'][factor]
                stats_factor += value

        self.redis_conn.set(self.stats_key, ujson.dumps(stats))
        logger.info(f'Saved tree stats. Trees count: {trees_count}')

    async def get_eco_stats(self) -> dict:
        value = await self.redis_conn.get(self.stats_key)
        return ujson.loads(value or '{}')
