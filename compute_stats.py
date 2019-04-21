from eco.utils import get_sync_redis_conn
from eco.stats import EcoStatistics


def compute_stats():
    redis_conn = get_sync_redis_conn()
    stats = EcoStatistics(redis_conn)
    stats.compute_stats()


if __name__ == '__main__':
    compute_stats()
