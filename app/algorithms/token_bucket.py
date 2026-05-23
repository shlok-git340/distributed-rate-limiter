import time

from app.storage.redis_client import redis_client
from app.config.runtime_config import CONFIG

class TokenBucketRateLimiter:

    def allow_request(
        self,
        identifier,
        route
    ):

        key = f"tb:{identifier}:{route}"

        bucket = redis_client.hgetall(key)

        current_time = time.time()

        capacity = CONFIG["limit"]

        refill_rate = capacity / CONFIG["window"]

        if not bucket:

            tokens = capacity
            last_refill = current_time

        else:

            tokens = float(bucket["tokens"])

            last_refill = float(
                bucket["last_refill"]
            )

            elapsed = current_time - last_refill

            refill = elapsed * refill_rate

            tokens = min(
                capacity,
                tokens + refill
            )

        if tokens < 1:
            return False

        tokens -= 1

        redis_client.hset(
            key,
            mapping={
                "tokens": tokens,
                "last_refill": current_time
            }
        )

        return True