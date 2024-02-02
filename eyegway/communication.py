from redis.asyncio import Redis
from redis.asyncio.client import Pipeline
import typing as t
from abc import ABC


class AsyncChannel(ABC):
    def __init__(
        self,
        redis: Redis,
        name: str,
        max_size: int = 0,
        push_method: str = "lpush",
        pop_method: t.Optional[str] = "brpop",
    ):
        """Generic async channel. It can be used as FIFO, LIFO or History channel by
        changing push and pop methods. The push method is used to push data to the
        channel, the pop method is used to pop data from the channel. The channel can
        be capped by max size. If the max size is reached, the oldest data is removed
        from the channel. If pop method is None, the channel is not allowed to pop data
        so can be used as a plain list with get method.

        Args:
            redis (Redis): the redis instance
            name (str): the name of the channel
            max_size (int, optional): the max size of the channel. Defaults to 0.
            push_method (str, optional): push method. Defaults to "lpush".
            pop_method (t.Optional[str], optional): pop method. Defaults to "brpop".
        """
        self.redis = redis
        self.channel_name = name
        self.max_size = max_size
        self.push_method = push_method
        self.pop_method = pop_method

    async def push(self, data: bytes, external_pipe: t.Optional[Pipeline] = None):
        pipe = self.redis.pipeline() if external_pipe is None else external_pipe
        await pipe.execute_command(self.push_method, self.channel_name, data)

        # trim the list if the max size is reached
        if self.max_size > 0:
            await pipe.ltrim(self.channel_name, 0, self.max_size - 1)

        if external_pipe is None:
            await pipe.execute()

    async def pop(self, timeout: int = 0) -> t.Optional[bytes]:
        if self.pop_method is None:
            raise PermissionError("pop method is not allowed for this channel")
        res = await self.redis.execute_command(
            self.pop_method,
            self.channel_name,
            timeout,
        )
        if res is None:
            return None
        _, payload = res
        return payload

    async def get(self, index: int) -> t.Optional[bytes]:
        return await self.redis.lindex(self.channel_name, index)

    async def slice(self, start: int, stop: int) -> t.List[bytes]:
        return await self.redis.lrange(self.channel_name, start, stop)

    async def size(self) -> int:
        return await self.redis.llen(self.channel_name)

    async def clear(self) -> None:
        await self.redis.delete(self.channel_name)


class AsyncFIFOChannel(AsyncChannel):
    def __init__(self, redis: Redis, name: str, max_size: int = 0):
        super().__init__(redis, name, max_size, "lpush", "brpop")


class AsyncLIFOChannel(AsyncChannel):
    def __init__(self, redis: Redis, name: str, max_size: int = 0):
        super().__init__(redis, name, max_size, "lpush", "blpop")


class AsyncHistoryChannel(AsyncChannel):
    def __init__(self, redis: Redis, name: str, max_size: int = 0):
        super().__init__(redis, name, max_size, "lpush", None)
