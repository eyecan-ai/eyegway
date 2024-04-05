from redis.asyncio import Redis
import typing as t
import pickle


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

    async def get(self) -> t.Optional[t.Any]:
        output = await self.redis.get(self.variable_name)
        if output is None:
            return None
        return pickle.loads(output)

    async def delete(self):
        await self.redis.delete(self.variable_name)
