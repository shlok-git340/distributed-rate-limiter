import time

from app.storage.redis_client import redis_client
from app.config.runtime_config import CONFIG

class FixedWindowRateLimiter:

    def allow_request(
        self,
        identifier,
        route
    ):

        current_window = (
            int(time.time())
            // CONFIG["window"]
        )

        key = (
            f"fw:{identifier}:{route}:{current_window}"
        )

        current_count = redis_client.incr(key)

        if current_count == 1:

            redis_client.expire(
                key,
                CONFIG["window"]
            )

        return current_count <= CONFIG["limit"]