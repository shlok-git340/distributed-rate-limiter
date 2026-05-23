import os

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = 6379

    RATE_LIMIT = 10
    WINDOW_SIZE = 60

    TOKEN_BUCKET_CAPACITY = 10
    TOKEN_REFILL_RATE = 1