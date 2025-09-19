-- KEYS[1]=key  ARGV[1]=capacity  ARGV[2]=refill_rate_per_sec  ARGV[3]=now  ARGV[4]=tokens_to_consume
local key        = KEYS[1]
local capacity   = tonumber(ARGV[1])
local rate       = tonumber(ARGV[2])
local now        = tonumber(ARGV[3])
local consume    = tonumber(ARGV[4])

local bucket = redis.call("HMGET", key, "tokens", "ts")
local tokens = tonumber(bucket[1])
local ts     = tonumber(bucket[2])

if tokens == nil then tokens = capacity end
if ts == nil then ts = now end

-- Refill
local delta = math.max(0, now - ts)
local filled = math.min(capacity, tokens + delta * rate)

local allowed = 0
if filled >= consume then
  tokens = filled - consume
  allowed = 1
else
  tokens = filled
end

redis.call("HMSET", key, "tokens", tokens, "ts", now)
-- set TTL to ~1h
redis.call("EXPIRE", key, 3600)

return {allowed, tokens}
