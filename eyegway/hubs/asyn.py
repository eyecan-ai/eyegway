from __future__ import annotations
import eyegway.packers as ecm
import eyegway.communication.async_channels as ecom
import eyegway.communication.async_variables as ecov
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
            eh.HubsParametrization.channel_buffer_name(name),
            max_buffer_size,
        )

        # History channel
        self.history = ecom.AsyncHistoryChannel(
            redis,
            eh.HubsParametrization.channel_history_name(name),
            max_history_size,
        )

        self._variables: t.Dict[str, ecov.AsyncSharedVariable] = {}
        self._history_frozen = self._create_variable("history_frozen", True)
        self._buffer_frozen = self._create_variable("buffer_frozen", True)

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
            if not await self.is_buffer_frozen():
                await self.buffer.push(data, pipe)
            if not await self.is_history_frozen():
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

    async def clear(self) -> None:
        await self.clear_buffer()
        await self.clear_history()

    async def freeze_history(self, status: bool = True) -> None:
        await self._history_frozen.set(status)

    async def freeze_buffer(self, status: bool = True) -> None:
        await self._buffer_frozen.set(status)

    async def freeze(self, status: bool = True) -> None:
        await self.freeze_buffer(status)
        await self.freeze_history(status)

    async def is_history_frozen(self) -> bool:
        return (await self._history_frozen.get()) is True

    async def is_buffer_frozen(self) -> bool:
        return (await self._buffer_frozen.get()) is True

    async def list_variables(self, include_privates: bool = False) -> t.List[str]:
        variables = await self.redis.keys(
            f"{eh.HubsParametrization.variable_name(self.name, '*')}"
        )
        variables = [variable.decode() for variable in variables]
        variables = eh.HubsParametrization.retrieve_variables_names_from_list(variables)
        if not include_privates:
            variables = [
                variable
                for variable in variables
                if not variable.startswith(
                    eh.HubsParametrization.PRIVATE_VARIABLE_PREFIX
                )
            ]
        return variables

    def _create_variable(
        self,
        name: str,
        private: bool = False,
    ) -> ecov.AsyncSharedVariable:
        variable_name = eh.HubsParametrization.variable_name(self.name, name, private)
        variable = ecov.AsyncSharedVariable(self.redis, variable_name)
        self._variables[name] = variable
        return variable

    def _get_variable(self, name: str) -> t.Optional[ecov.AsyncSharedVariable]:
        if name not in self._variables:
            return None
        return self._variables[name]

    async def set_variable_value(self, name: str, value: t.Any) -> None:
        variable = self._get_variable(name)
        if variable is None:
            variable = self._create_variable(name, False)
        await variable.set(value)

    async def get_variable_value(self, name: str) -> t.Optional[t.Any]:
        variable = self._get_variable(name)
        if variable is None:
            variable = self._create_variable(name, False)
        return await variable.get()

    async def delete_variable(self, name: str) -> None:
        variable = self._create_variable(name, False)
        await variable.delete()
        if name in self._variables:
            del self._variables[name]

    @staticmethod
    def create(
        name: str,
        config: t.Optional[eh.HubsConfig] = None,
        redis: t.Optional[Redis] = None,
    ) -> AsyncMessageHub:
        if config is None:
            config = eh.HubsConfig()

        return AsyncMessageHub(
            redis or eh.HubsConfig.create_redis_async_instance(config),
            name,
            ecp.PackersFactory.create(config.packer),
            config.max_buffer_size,
            config.max_history_size,
            config.max_payload_size,
        )


class AsyncMessageHubManager:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def list(self) -> t.List[str]:
        channels = await self.redis.keys(f"{eh.HubsParametrization.HUBS_PREFIX}*")
        channels = [channel.decode() for channel in channels]
        return eh.HubsParametrization.retrieve_hubs_names_from_channel_list(channels)

    @staticmethod
    def create(
        config: t.Optional[eh.HubsConfig] = None,
        redis: t.Optional[Redis] = None,
    ) -> AsyncMessageHubManager:
        if config is None:
            config = eh.HubsConfig()

        return AsyncMessageHubManager(
            redis=redis or eh.HubsConfig.create_redis_async_instance(config)
        )
