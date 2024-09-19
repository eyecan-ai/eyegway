from __future__ import annotations
import pydantic as pyd
import typing as t


class HubsParametrization:
    FAKE_REDIS_NAME = "fakeredis"
    SEPARATOR = ":"
    HUBS_PREFIX = f"eyegway{SEPARATOR}hubs{SEPARATOR}"
    HUBS_VARIABLES_PREFIX = f"eyegway{SEPARATOR}hubs_variables{SEPARATOR}"
    BUFFER_NAME = "buffer"
    HISTORY_NAME = "history"
    VARIABLE_SEPARATOR = "#"
    PRIVATE_VARIABLE_PREFIX = "_"

    @classmethod
    def hub_name(cls, hub_name: str) -> str:
        return f"{cls.HUBS_PREFIX}{hub_name}"

    @classmethod
    def channel_name(cls, hub_name: str, channel_name: str) -> str:
        return f"{cls.hub_name(hub_name)}{cls.SEPARATOR}{channel_name}"

    @classmethod
    def channel_buffer_name(cls, hub_name: str) -> str:
        return cls.channel_name(hub_name, cls.BUFFER_NAME)

    @classmethod
    def channel_history_name(cls, hub_name: str) -> str:
        return cls.channel_name(hub_name, cls.HISTORY_NAME)

    @classmethod
    def retrieve_hubs_names_from_channel_list(
        cls, channels: t.List[str]
    ) -> t.List[str]:
        channels = [channel.replace(cls.HUBS_PREFIX, "") for channel in channels]
        channels = [channel.split(cls.SEPARATOR)[0] for channel in channels]
        return list(set(channels))

    @classmethod
    def variable_name(
        cls, hub_name: str, variable_name: str, private: bool = False
    ) -> str:
        prefix = cls.PRIVATE_VARIABLE_PREFIX if private else ""
        return (
            f"{cls.HUBS_VARIABLES_PREFIX}{hub_name}"
            f"{cls.VARIABLE_SEPARATOR}{prefix}{variable_name}"
        )

    @classmethod
    def retrieve_variables_names_from_list(cls, variables: t.List[str]) -> t.List[str]:
        variables = [
            variable.replace(cls.HUBS_VARIABLES_PREFIX, "") for variable in variables
        ]
        variables = [
            variable.split(cls.VARIABLE_SEPARATOR)[1] for variable in variables
        ]
        return list(set(variables))


class HubsConfig(pyd.BaseSettings):
    max_buffer_size: int = 64
    max_history_size: int = 64
    max_payload_size: int = 64_000_000
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_username: t.Optional[str] = None
    redis_password: t.Optional[str] = None
    redis_extra_options: t.Mapping[str, t.Any] = pyd.Field(default_factory=dict)
    packer: t.Optional[str] = None

    class Config:
        env_prefix = "eyegway_hubs_"

    @classmethod
    def create_redis_async_instance(cls, config: HubsConfig) -> t.Any:
        if config.redis_host == HubsParametrization.FAKE_REDIS_NAME:
            import fakeredis

            return fakeredis.FakeAsyncRedis()
        else:
            from redis.asyncio import Redis

            return Redis(
                host=config.redis_host,
                port=config.redis_port,
                username=config.redis_username,
                password=config.redis_password,
                **config.redis_extra_options,
            )

    @classmethod
    def create_redis_instance(cls, config: HubsConfig) -> t.Any:
        if config.redis_host == HubsParametrization.FAKE_REDIS_NAME:
            import fakeredis

            return fakeredis.FakeRedis()
        else:
            from redis import Redis

            return Redis(
                host=config.redis_host,
                port=config.redis_port,
                username=config.redis_username,
                password=config.redis_password,
                **config.redis_extra_options,
            )
