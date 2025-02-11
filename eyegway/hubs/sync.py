from __future__ import annotations

import typing as t

from redis import Redis

import eyegway.communication.channels as ecom
import eyegway.communication.variables as ecov
import eyegway.hubs as eh
import eyegway.hubs.connectors as ehc
import eyegway.packers as ecm
import eyegway.packers.factory as ecp
import eyegway.utils as eut


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
            eh.HubsParametrization.channel_buffer_name(name),
            max_buffer_size,
        )

        # History channel
        self.history = ecom.HistoryChannel(
            redis,
            eh.HubsParametrization.channel_history_name(name),
            max_history_size,
        )

        self._variables: t.Mapping[str, ecov.SharedVariable] = {}
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

    def push(self, obj: t.Any) -> None:
        obj = self.world_to_hub(obj)
        with eut.LoguruTimer("HUB Packing"):
            data = self.packer.pack(obj)

        if self.max_payload_size > 0 and len(data) > self.max_payload_size:
            raise ValueError(f"Payload too big [Max: {self.max_payload_size}]")

        with eut.LoguruTimer("HUB Pushing"):
            pipe = self.redis.pipeline()
            if not self.is_buffer_frozen():
                self.buffer.push(data, pipe)
            if not self.is_history_frozen():
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

    def clear(self) -> None:
        self.clear_buffer()
        self.clear_history()

    def freeze_history(self, status: bool = True) -> None:
        self._history_frozen.set(status)

    def freeze_buffer(self, status: bool = True) -> None:
        self._buffer_frozen.set(status)

    def is_history_frozen(self) -> bool:
        return self._history_frozen.get() is True

    def is_buffer_frozen(self) -> bool:
        return self._buffer_frozen.get() is True

    def freeze(self, status: bool = True) -> None:
        self.freeze_buffer(status)
        self.freeze_history(status)

    def list_variables(self, include_privates: bool = False) -> t.List[str]:
        variables = self.redis.keys(
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
    ) -> ecov.SharedVariable:
        variable_name = eh.HubsParametrization.variable_name(self.name, name, private)
        variable = ecov.SharedVariable(self.redis, variable_name)
        self._variables[name] = variable
        return variable

    def _get_variable(self, name: str) -> t.Optional[ecov.SharedVariable]:
        if name not in self._variables:
            return None
        return self._variables[name]

    def set_variable_value(self, name: str, value: t.Any) -> None:
        variable = self._get_variable(name)
        if variable is None:
            variable = self._create_variable(name, False)
        variable.set(value)

    def get_variable_value(self, name: str) -> t.Optional[t.Any]:
        variable = self._get_variable(name)
        if variable is None:
            variable = self._create_variable(name, False)
        return variable.get()

    def delete_variable(self, name: str) -> None:
        variable = self._create_variable(name, False)
        variable.delete()
        if name in self._variables:
            del self._variables[name]

    @staticmethod
    def create(
        name: t.Optional[str] = None,
        config: t.Optional[eh.HubsConfig] = None,
        redis: t.Optional[Redis] = None,
    ) -> MessageHub:
        if config is None:
            config = eh.HubsConfig()

        return MessageHub(
            redis or eh.HubsConfig.create_redis_instance(config),
            name or config.hub_name,
            ecp.PackersFactory.create(config.packer),
            config.max_buffer_size,
            config.max_history_size,
            config.max_payload_size,
        )


class MessageHubManager:

    def __init__(self, redis: Redis):
        self.redis = redis

    def list(self) -> t.List[str]:
        channels = self.redis.keys(f"{eh.HubsParametrization.HUBS_PREFIX}*")
        channels = [channel.decode() for channel in channels]
        return eh.HubsParametrization.retrieve_hubs_names_from_channel_list(channels)

    @staticmethod
    def create(
        config: t.Optional[eh.HubsConfig] = None,
        redis: t.Optional[Redis] = None,
    ) -> MessageHubManager:
        if config is None:
            config = eh.HubsConfig()

        return MessageHubManager(
            redis=(
                eh.HubsConfig.create_redis_instance(config) if redis is None else redis
            )
        )
