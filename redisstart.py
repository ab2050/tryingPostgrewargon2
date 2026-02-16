import redis

# docker container name is focused-napier
red = redis.Redis(host="localhost", port = 6379, decode_responses=True)