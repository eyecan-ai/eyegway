from __future__ import annotations
from redis.asyncio import Redis
import eyegway.communication as ecom
import eyegway.commons as ecm
import eyegway.utils as eut
import typing as t
import pydantic as pyd


class MessageHubConfig(pyd.BaseSettings):
    max_buffer_size: int = 64
    max_history_size: int = 64
    max_payload_size: int = 64_000_000
    redis_host: str = "localhost"
    redis_port: int = 6379
    parsers_string: t.Optional[str] = (
        '(...,...,3) uint8 > image/jpeg | '
        + '(...,...) uint8 > image/png | '
        + 'numpy2tensor'
    )

    class Config:
        env_prefix = "EYEGWAY_MESSAGE_HUB_"


class AsyncMessageHub:

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
        with eut.LoguruTimer("HUB Packing"):
            data = self.packer.pack(obj)

        if self.max_payload_size > 0 and len(data) > self.max_payload_size:
            raise ValueError(f"Payload too big [Max: {self.max_payload_size}]")

        with eut.LoguruTimer("HUB Pushing"):
            pipe = self.redis.pipeline()
            await self.buffer.push(data, pipe)
            await self.history.push(data, pipe)
            await pipe.execute()

    async def pop_raw(self, timeout: int = 0) -> t.Optional[bytes]:
        return await self.buffer.pop(timeout)

    async def pop(self, timeout: int = 0) -> t.Optional[t.Any]:
        data = await self.pop_raw(timeout)
        if data is None:
            return None
        return self.packer.unpack(data)

    async def last_raw(self, offset: int = 0) -> t.Optional[bytes]:
        return await self.history.get(offset)

    async def last(self, offset: int = 0) -> t.Optional[bytes]:
        data = await self.last_raw(offset)
        if data is None:
            return None
        return self.packer.unpack(data)

    async def last_multiple_raw(self, start: int, stop: int) -> t.List[bytes]:
        datas = await self.history.slice(start, stop)
        return datas

    async def last_multiple(self, start: int, stop: int) -> t.List[bytes]:
        datas = await self.last_multiple_raw(start, stop)
        return [self.packer.unpack(data) for data in datas]

    async def history_size(self) -> int:
        return await self.history.size()

    async def buffer_size(self) -> int:
        return await self.buffer.size()

    async def clear_buffer(self) -> None:
        await self.buffer.clear()

    async def clear_history(self) -> None:
        await self.history.clear()

    @staticmethod
    def create(
        name: str, config: t.Optional[MessageHubConfig] = None
    ) -> AsyncMessageHub:
        if config is None:
            config = MessageHubConfig()

        redis = Redis(host=config.redis_host, port=config.redis_port)
        import eyegway.packaging as ecp

        return AsyncMessageHub(
            redis,
            name,
            ecp.DefaultMsgPacker(parsers_string=config.parsers_string),
            config.max_buffer_size,
            config.max_history_size,
            config.max_payload_size,
        )
