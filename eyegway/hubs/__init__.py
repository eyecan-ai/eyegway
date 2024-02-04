import pydantic as pyd
import typing as t


class HubsConfig(pyd.BaseSettings):
    max_buffer_size: int = 64
    max_history_size: int = 64
    max_payload_size: int = 64_000_000
    redis_host: str = "localhost"
    redis_port: int = 6379
    packer: t.Optional[str] = "default"

    class Config:
        env_prefix = "EYEGWAY_MESSAGE_HUB_"
