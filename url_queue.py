import redis
import config

# LATER USE FUNC
r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

async def enqueue_url(url):
    r.lpush("crawling_queue", url)

async def dequeue_url():
    url = r.rpop("crawling_queue")
    return url.decode("utf-8") if url else None