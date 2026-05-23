import time

from app.storage.redis_client import redis_client
from app.config.runtime_config import CONFIG

class SlidingWindowCounterRateLimiter:

    def allow_request(
        self,
        identifier,
        route
    ):

        now = time.time()

        window = CONFIG["window"]
        limit = CONFIG["limit"]

        current_window = int(now // window)

        previous_window = current_window - 1

        current_key = (
            f"sw:{identifier}:{route}:{current_window}"
        )

        previous_key = (
            f"sw:{identifier}:{route}:{previous_window}"
        )

        current_count = redis_client.get(current_key)
        previous_count = redis_client.get(previous_key)

        current_count = int(current_count or 0)
        previous_count = int(previous_count or 0)

        elapsed = now % window

        weight = (window - elapsed) / window

        total = previous_count * weight + current_count

        if total >= limit:
            return False

        redis_client.incr(current_key)

        redis_client.expire(
            current_key,
            window * 2
        )

        return True