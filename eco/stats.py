import ujson
from typing import Dict, Any

from sqlalchemy import Column, Integer, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

from eco import config
from eco.data_utils import load_models
from eco.eco_model import predict_all_benefits
from eco.utils import session_scope

Base = declarative_base()  # type: Any
conn = f'postgresql+psycopg2://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}'
engine = create_engine(conn)
Base.metadata.bind = engine


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
            trees = session.query(Tree).filter_by(instance_id=1).all()
            return [t.diameter for t in trees if t.diameter]


class EcoStatistics:
    stats_key = 'eco_stats'
    db_backend = OTMDatabaseBackend

    def __init__(self, redis_conn) -> None:
        self.redis_conn = redis_conn
        self.db = self.db_backend()
        self.eco_models = load_models(config.MODELS_PATH)

    def compute_stats(self) -> None:
        """
        Fetches all trees from the external database
        and stores total eco statistics in Redis.
        """
        trees = self.db.get_trees()
        stats: Dict[str, Any] = {
            'benefits': {
                'NO2': 0.0,
                'O3': 0.0,
                'PM2.5': 0.0,
                'SO2': 0.0,
            },
            'trees_count': len(trees),
        }

        for diam in trees:
            benefits = predict_all_benefits(self.eco_models, diam)
            for factor, value in benefits.items():
                stats_factor = stats['benefits'][factor]
                stats_factor += value

        self.redis_conn.set(self.stats_key, ujson.dumps(stats))

    async def get_eco_stats(self) -> dict:
        value = await self.redis_conn.get(self.stats_key)
        return ujson.loads(value or '{}')
