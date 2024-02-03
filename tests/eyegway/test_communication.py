import redis.asyncio as aioredis
import eyegway.communication as ecom
import pytest


class TestChannels:

    @pytest.mark.asyncio
    async def test_fifo_channels(self, redis_test_mock_async: aioredis.Redis):

        max_size = 100
        channel = ecom.AsyncFIFOChannel(
            redis_test_mock_async,
            "test",
            max_size=max_size,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]

        # Push all messages and pop them
        for idx in range(max_size):
            await channel.push(messages[idx])
        assert await channel.size() == max_size
        for idx in range(max_size):
            assert await channel.pop() == messages[idx]

        # Push double the messages and pop them
        for idx in range(max_size * 2):
            await channel.push(messages[idx % max_size])
        assert await channel.size() == max_size

        for idx in range(max_size):
            assert await channel.pop(1)

        assert await channel.pop(1) is None

    @pytest.mark.asyncio
    async def test_empty_fifo_channels(self, redis_test_mock_async: aioredis.Redis):

        max_size = 100
        channel = ecom.AsyncFIFOChannel(
            redis_test_mock_async,
            "test",
            max_size=0,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]

        # Push all messages and pop them
        for idx in range(max_size):
            await channel.push(messages[idx])
        assert await channel.size() == 0

    @pytest.mark.asyncio
    async def test_lifo_channels(self, redis_test_mock_async: aioredis.Redis):

        max_size = 100
        channel = ecom.AsyncLIFOChannel(
            redis_test_mock_async,
            "test",
            max_size=max_size,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]
        reversed_messages = messages[::-1]

        # Push all messages and pop them
        for idx in range(max_size):
            await channel.push(messages[idx])
        assert await channel.size() == max_size
        for idx in range(max_size):
            assert await channel.pop() == reversed_messages[idx]

        # Push double the messages and pop them
        for idx in range(max_size * 2):
            await channel.push(messages[idx % max_size])
        assert await channel.size() == max_size

        for idx in range(max_size):
            assert await channel.pop(1)

        assert await channel.pop(1) is None

    @pytest.mark.asyncio
    async def test_history_channels(self, redis_test_mock_async: aioredis.Redis):

        max_size = 100
        channel = ecom.AsyncHistoryChannel(
            redis_test_mock_async,
            "test",
            max_size=max_size,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]
        reversed_messages = messages[::-1]

        # Push all messages and pop them
        for idx in range(max_size):
            await channel.push(messages[idx])

        assert await channel.size() == max_size

        # Push all messages and pop them
        with pytest.raises(PermissionError):
            await channel.pop()

        for idx in range(max_size):
            assert await channel.get(idx) == reversed_messages[idx]

        assert await channel.slice(0, max_size - 1) == reversed_messages

        assert await channel.get(max_size) == None

        await channel.clear()

        assert await channel.size() == 0
