
from src.config import Config
from redis.asyncio import Redis

JTI_EXPIRY = 3600

# token_blocklist = aioredis.from_url(
#     Config.REDIS_URL
#     # encoding="utf-8",
#     # decode_responses=True
# )


token_blocklist = Redis.from_url(Config.REDIS_URL)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None