import redis.asyncio as redis

# Asynchronous function to connect to Redis.
async def get_redis():
    """
    Establishes an asynchronous connection to the Redis service.

    This function creates and returns an instance of a Redis connection
    that can be used to interact with a Redis database. It uses the `from_url`
    method from the `redis.asyncio` library to connect to a Redis service
    running at the specified URL (in this case, the default connection to Redis
    at `redis://redis:6379`).

    The connection is configured to decode responses to strings.

    Returns:
        Redis: An instance of the Redis connection client, which can be used 
               for interacting with Redis asynchronously.
    """
    return redis.from_url("redis://redis:6379", decode_responses=True)
