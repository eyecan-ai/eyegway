import loguru
from redis import Redis
from redis.client import Pipeline
import typing as t
from abc import ABC


class Channel(ABC):
    def __init__(
        self,
        redis: Redis,
        name: str,
        max_size: int = -1,
        push_method: str = "lpush",
        pop_method: t.Optional[str] = "brpop",
    ):
        """Generic  channel. It can be used as FIFO, LIFO or History channel by
        changing push and pop methods. The push method is used to push data to the
        channel, the pop method is used to pop data from the channel. The channel can
        be capped by max size. If the max size is reached, the oldest data is removed
        from the channel. If pop method is None, the channel is not allowed to pop data
        so can be used as a plain list with get method.

        Args:
            redis (Redis): the redis instance
            name (str): the name of the channel
            max_size (int, optional): the max size of the channel (-1 for unlimited).
                Defaults to -1.
            push_method (str, optional): push method. Defaults to "lpush".
            pop_method (t.Optional[str], optional): pop method. Defaults to "brpop".
        """
        self.redis = redis
        self.channel_name = name
        self.max_size = max_size
        self.push_method = push_method
        self.pop_method = pop_method

    def push(self, data: bytes, external_pipe: t.Optional[Pipeline] = None):
        if self.max_size == 0:
            return

        pipe = self.redis.pipeline() if external_pipe is None else external_pipe
        pipe.execute_command(self.push_method, self.channel_name, data)

        # trim the list if the max size is reached
        if self.max_size > 0:
            pipe.ltrim(self.channel_name, 0, self.max_size - 1)
        else:  # pragma: no cover
            loguru.logger.warning("Max size is not set for channel {self.channel_name}")

        if external_pipe is None:
            pipe.execute()

    def pop(self, timeout: int = 0) -> t.Optional[bytes]:
        if self.pop_method is None:
            raise PermissionError("pop method is not allowed for this channel")
        res = self.redis.execute_command(
            self.pop_method,
            self.channel_name,
            timeout,
        )
        if res is None:
            return None
        _, payload = res
        return payload

    def get(self, index: int) -> t.Optional[bytes]:
        return self.redis.lindex(self.channel_name, index)

    def slice(self, start: int, stop: int) -> t.List[bytes]:
        return self.redis.lrange(self.channel_name, start, stop)

    def size(self) -> int:
        return self.redis.llen(self.channel_name)

    def clear(self) -> None:
        self.redis.delete(self.channel_name)


class FIFOChannel(Channel):
    def __init__(self, redis: Redis, name: str, max_size: int = 0):
        super().__init__(redis, name, max_size, "lpush", "brpop")


class LIFOChannel(Channel):
    def __init__(self, redis: Redis, name: str, max_size: int = 0):
        super().__init__(redis, name, max_size, "lpush", "blpop")


class HistoryChannel(Channel):
    def __init__(self, redis: Redis, name: str, max_size: int = 0):
        super().__init__(redis, name, max_size, "lpush", None)
