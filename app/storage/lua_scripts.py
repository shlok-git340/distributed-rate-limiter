SLIDING_WINDOW_LUA = """

local key = KEYS[1]

local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])

redis.call(
    "ZREMRANGEBYSCORE",
    key,
    0,
    current_time - window
)

local count = redis.call(
    "ZCARD",
    key
)

if count >= limit then
    return 0
end

redis.call(
    "ZADD",
    key,
    current_time,
    current_time
)

redis.call(
    "EXPIRE",
    key,
    window
)

return 1
"""