import redis
import eyegway.communication.channels as ecom
import pytest


class TestChannels:

    def test_fifo_channels(self, redis_test_mock_sync: redis.Redis):

        max_size = 100
        channel = ecom.FIFOChannel(
            redis_test_mock_sync,
            "test",
            max_size=max_size,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]

        # Push all messages and pop them
        for idx in range(max_size):
            channel.push(messages[idx])
        assert channel.size() == max_size
        for idx in range(max_size):
            assert channel.pop() == messages[idx]

        # Push double the messages and pop them
        for idx in range(max_size * 2):
            channel.push(messages[idx % max_size])
        assert channel.size() == max_size

        for idx in range(max_size):
            assert channel.pop(1)

        assert channel.pop(1) is None

    def test_empty_fifo_channels(self, redis_test_mock_sync: redis.Redis):

        max_size = 100
        channel = ecom.FIFOChannel(
            redis_test_mock_sync,
            "test",
            max_size=0,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]

        # Push all messages and pop them
        for idx in range(max_size):
            channel.push(messages[idx])
        assert channel.size() == 0

    def test_lifo_channels(self, redis_test_mock_sync: redis.Redis):

        max_size = 100
        channel = ecom.LIFOChannel(
            redis_test_mock_sync,
            "test",
            max_size=max_size,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]
        reversed_messages = messages[::-1]

        # Push all messages and pop them
        for idx in range(max_size):
            channel.push(messages[idx])
        assert channel.size() == max_size
        for idx in range(max_size):
            assert channel.pop() == reversed_messages[idx]

        # Push double the messages and pop them
        for idx in range(max_size * 2):
            channel.push(messages[idx % max_size])
        assert channel.size() == max_size

        for idx in range(max_size):
            assert channel.pop(1)

        assert channel.pop(1) is None

    def test_history_channels(self, redis_test_mock_sync: redis.Redis):

        max_size = 100
        channel = ecom.HistoryChannel(
            redis_test_mock_sync,
            "test",
            max_size=max_size,
        )

        messages = [f"msg-{idx}".encode('utf-8') for idx in range(max_size)]
        reversed_messages = messages[::-1]

        # Push all messages and pop them
        for idx in range(max_size):
            channel.push(messages[idx])

        assert channel.size() == max_size

        # Push all messages and pop them
        with pytest.raises(PermissionError):
            channel.pop()

        for idx in range(max_size):
            assert channel.get(idx) == reversed_messages[idx]

        assert channel.slice(0, max_size - 1) == reversed_messages

        assert channel.get(max_size) is None

        channel.clear()

        assert channel.size() == 0
