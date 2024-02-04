from __future__ import annotations
import eyegway.packers as ecm
import eyegway.communication.async_channels as ecom
import eyegway.packers.factory as ecp
import eyegway.utils as eut
import eyegway.hubs as eh
import eyegway.hubs.connectors as ehc
from redis.asyncio import Redis


import typing as t


class AsyncMessageHub:

    def __init__(
        self,
        redis: Redis,
        name: str,
        packer: ecm.Packer,
        max_buffer_size: int = 0,
        max_history_size: int = 0,
        max_payload_size: int = 0,
        connectors: t.Optional[t.List[ehc.HubConnector]] = None,
    ):
        self.redis = redis
        self.name = name
        self.max_buffer_size = max_buffer_size
        self.max_history_size = max_history_size
        self.max_payload_size = max_payload_size
        self.packer = packer
        self.connectors = connectors or []

        # Buffer channel
        self.buffer = ecom.AsyncFIFOChannel(
            redis,
            f"{name}:buffer",
            max_buffer_size,
        )

        # History channel
        self.history = ecom.AsyncHistoryChannel(
            redis,
            f"{name}:history",
            max_history_size,
        )

    def world_to_hub(self, data: t.Any) -> t.Any:
        input_data = data
        for connector in self.connectors:
            input_data = connector.world_to_hub(input_data)
        return input_data

    def hub_to_world(self, data: t.Any) -> t.Any:
        output_data = data
        for connector in self.connectors:
            output_data = connector.hub_to_world(output_data)
        return output_data

    async def push_raw(self, data: bytes) -> None:
        with eut.LoguruTimer("HUB Pushing"):
            pipe = self.redis.pipeline()
            await self.buffer.push(data, pipe)
            await self.history.push(data, pipe)
            await pipe.execute()

    async def push(self, obj: t.Any) -> None:
        obj = self.world_to_hub(obj)
        with eut.LoguruTimer("HUB Packing"):
            data = self.packer.pack(obj)

        if self.max_payload_size > 0 and len(data) > self.max_payload_size:
            raise ValueError(f"Payload too big [Max: {self.max_payload_size}]")

        await self.push_raw(data)

    async def pop_raw(self, timeout: int = 0) -> t.Optional[bytes]:
        return await self.buffer.pop(timeout)

    async def pop(self, timeout: int = 0) -> t.Optional[t.Any]:
        data = await self.pop_raw(timeout)
        if data is None:
            return None
        return self.hub_to_world(self.packer.unpack(data))

    async def last_raw(self, offset: int = 0) -> t.Optional[bytes]:
        return await self.history.get(offset)

    async def last(self, offset: int = 0) -> t.Optional[t.Any]:
        data = await self.last_raw(offset)
        if data is None:
            return None
        return self.hub_to_world(self.packer.unpack(data))

    async def last_multiple_raw(self, start: int, stop: int) -> t.List[bytes]:
        datas = await self.history.slice(start, stop)
        return datas

    async def last_multiple(self, start: int, stop: int) -> t.List[t.Any]:
        datas = await self.last_multiple_raw(start, stop)
        return [self.hub_to_world(self.packer.unpack(data)) for data in datas]

    async def history_size(self) -> int:
        return await self.history.size()

    async def buffer_size(self) -> int:
        return await self.buffer.size()

    async def clear_buffer(self) -> None:
        await self.buffer.clear()

    async def clear_history(self) -> None:
        await self.history.clear()

    @staticmethod
    def create(name: str, config: t.Optional[eh.HubsConfig] = None) -> AsyncMessageHub:
        if config is None:
            config = eh.HubsConfig()

        if config.redis_host == 'fakeredis':
            import fakeredis

            redis = fakeredis.FakeAsyncRedis()
        else:
            redis = Redis(host=config.redis_host, port=config.redis_port)

        return AsyncMessageHub(
            redis,
            name,
            ecp.PackersFactory.create(config.packer),
            config.max_buffer_size,
            config.max_history_size,
            config.max_payload_size,
        )
