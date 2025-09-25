import aioredis
from src.config import Config

JTI_EXPIRY = 3600

token_blocklist = aioredis.from_url(
    f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0",
    encoding="utf-8",
    decode_responses=True
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None