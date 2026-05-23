import time

from app.storage.redis_client import redis_client
from app.storage.lua_scripts import (
    SLIDING_WINDOW_LUA
)

class SlidingLogRateLimiter:

    def allow_request(self, identifier, route):

        key = f"sl:{identifier}:{route}"

        result = redis_client.eval(
            SLIDING_WINDOW_LUA,
            1,
            key,
            10,
            60,
            time.time()
        )

        return result == 1