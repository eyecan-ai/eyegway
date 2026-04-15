import pickle
import typing as t

from redis.asyncio import Redis


class AsyncSharedVariable:
    def __init__(
        self,
        redis: Redis,
        name: str,
    ):
        self.redis = redis
        self.variable_name = name

    async def set(self, value: t.Any):
        await self.redis.set(self.variable_name, pickle.dumps(value))

    async def get(self) -> t.Any | None:
        output = await self.redis.get(self.variable_name)
        if output is None:
            return None
        return pickle.loads(output)

    async def delete(self):
        await self.redis.delete(self.variable_name)
