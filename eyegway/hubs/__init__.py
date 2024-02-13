from __future__ import annotations
import pydantic as pyd
import typing as t


class HubsParametrization:
    FAKE_REDIS_NAME = "fakeredis"
    SEPARATOR = ":"
    HUBS_PREFIX = f"eyegway{SEPARATOR}hubs{SEPARATOR}"
    BUFFER_NAME = "buffer"
    HISTORY_NAME = "history"

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


class HubsConfig(pyd.BaseSettings):
    max_buffer_size: int = 64
    max_history_size: int = 64
    max_payload_size: int = 64_000_000
    redis_host: str = "localhost"
    redis_port: int = 6379
    packer: t.Optional[str] = "default"

    class Config:
        env_prefix = "EYEGWAY_MESSAGE_HUB_"

    @classmethod
    def create_redis_async_instance(cls, config: HubsConfig) -> t.Any:
        if config.redis_host == HubsParametrization.FAKE_REDIS_NAME:
            import fakeredis

            return fakeredis.FakeAsyncRedis()
        else:
            from redis.asyncio import Redis

            return Redis(host=config.redis_host, port=config.redis_port)

    @classmethod
    def create_redis_instance(cls, config: HubsConfig) -> t.Any:
        if config.redis_host == HubsParametrization.FAKE_REDIS_NAME:
            import fakeredis

            return fakeredis.FakeRedis()
        else:
            from redis import Redis

            return Redis(host=config.redis_host, port=config.redis_port)
