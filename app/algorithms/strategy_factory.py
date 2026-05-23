from app.config.runtime_config import CONFIG

from app.algorithms.fixed_window import (
    FixedWindowRateLimiter
)

from app.algorithms.token_bucket import (
    TokenBucketRateLimiter
)

from app.algorithms.sliding_window_counter import (
    SlidingWindowCounterRateLimiter
)

def get_rate_limiter():

    algorithm = CONFIG["algorithm"]

    if algorithm == "fixed_window":
        return FixedWindowRateLimiter()

    if algorithm == "token_bucket":
        return TokenBucketRateLimiter()

    return SlidingWindowCounterRateLimiter()