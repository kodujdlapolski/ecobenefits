from eco.stats import EcoStatistics
from eco.utils import get_sync_redis_conn


def compute_stats():
    redis_conn = get_sync_redis_conn()
    stats = EcoStatistics(redis_conn)
    stats.compute_stats()


if __name__ == '__main__':
    compute_stats()
