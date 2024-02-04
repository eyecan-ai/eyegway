from __future__ import annotations
import eyegway.packers as ecm
import eyegway.communication.channels as ecom
import eyegway.packers.factory as ecp
import eyegway.utils as eut
import eyegway.hubs as eh
import eyegway.hubs.connectors as ehc
from redis import Redis
import typing as t


class MessageHub:

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
        self.buffer = ecom.FIFOChannel(
            redis,
            f"{name}:buffer",
            max_buffer_size,
        )

        # History channel
        self.history = ecom.HistoryChannel(
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

    def push(self, obj: t.Any) -> None:
        obj = self.world_to_hub(obj)
        with eut.LoguruTimer("HUB Packing"):
            data = self.packer.pack(obj)

        if self.max_payload_size > 0 and len(data) > self.max_payload_size:
            raise ValueError(f"Payload too big [Max: {self.max_payload_size}]")

        with eut.LoguruTimer("HUB Pushing"):
            pipe = self.redis.pipeline()
            self.buffer.push(data, pipe)
            self.history.push(data, pipe)
            pipe.execute()

    def pop_raw(self, timeout: int = 0) -> t.Optional[bytes]:
        return self.buffer.pop(timeout)

    def pop(self, timeout: int = 0) -> t.Optional[t.Any]:
        data = self.pop_raw(timeout)
        if data is None:
            return None
        return self.hub_to_world(self.packer.unpack(data))

    def last_raw(self, offset: int = 0) -> t.Optional[bytes]:
        return self.history.get(offset)

    def last(self, offset: int = 0) -> t.Optional[t.Any]:
        data = self.last_raw(offset)
        if data is None:
            return None
        return self.hub_to_world(self.packer.unpack(data))

    def last_multiple_raw(self, start: int, stop: int) -> t.List[bytes]:
        datas = self.history.slice(start, stop)
        return datas

    def last_multiple(self, start: int, stop: int) -> t.List[t.Any]:
        datas = self.last_multiple_raw(start, stop)
        return [self.hub_to_world(self.packer.unpack(data)) for data in datas]

    def history_size(self) -> int:
        return self.history.size()

    def buffer_size(self) -> int:
        return self.buffer.size()

    def clear_buffer(self) -> None:
        self.buffer.clear()

    def clear_history(self) -> None:
        self.history.clear()

    @staticmethod
    def create(name: str, config: t.Optional[eh.HubsConfig] = None) -> MessageHub:
        if config is None:
            config = eh.HubsConfig()

        if config.redis_host == 'fakeredis':
            import fakeredis

            redis = fakeredis.FakeRedis()
        else:
            redis = Redis(host=config.redis_host, port=config.redis_port)

        return MessageHub(
            redis,
            name,
            ecp.PackersFactory.create(config.packer),
            config.max_buffer_size,
            config.max_history_size,
            config.max_payload_size,
        )
