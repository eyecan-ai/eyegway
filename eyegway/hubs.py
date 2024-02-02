from redis.asyncio import Redis
import eyegway.communication as ecom
import eyegway.commons as ecm
import typing as t


class SimpleMessageHub:

    def __init__(
        self,
        redis: Redis,
        name: str,
        packer: ecm.Packer,
        max_buffer_size: int = 0,
        max_history_size: int = 0,
        max_payload_size: int = 0,
    ):
        self.redis = redis
        self.name = name
        self.max_buffer_size = max_buffer_size
        self.max_history_size = max_history_size
        self.max_payload_size = max_payload_size
        self.packer = packer
        self.buffer = ecom.AsyncFIFOChannel(redis, f"{name}:buffer", max_buffer_size)
        self.history = ecom.AsyncHistoryChannel(
            redis, f"{name}:history", max_history_size
        )

    async def push(self, obj: t.Any) -> None:
        data = self.packer.pack(obj)
        if self.max_payload_size > 0 and len(data) > self.max_payload_size:
            raise ValueError("Payload too big")
        pipe = self.redis.pipeline()
        await self.buffer.push(data, pipe)
        await self.history.push(data, pipe)
        await pipe.execute()

    async def pop(self, timeout: int = 0) -> t.Optional[t.Any]:
        data = await self.buffer.pop(timeout)
        if data is None:
            return None
        return self.packer.unpack(data)

    async def last(self, start: int = 0) -> t.Optional[bytes]:
        data = await self.history.get(start)
        if data is None:
            return None
        return self.packer.unpack(data)

    async def last_multiple(self, start: int, stop: int) -> t.List[bytes]:
        datas = await self.history.slice(start, stop)
        return [self.packer.unpack(data) for data in datas]

    async def history_size(self) -> int:
        return await self.history.size()

    async def buffer_size(self) -> int:
        return await self.buffer.size()

    async def clear_buffer(self) -> None:
        await self.buffer.clear()

    async def clear_history(self) -> None:
        await self.history.clear()
