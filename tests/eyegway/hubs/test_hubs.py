import eyegway.hubs as eh
import eyegway.hubs.asyn as eha
import eyegway.packers as ecm
import redis.asyncio as aioredis
import pytest


class TestMessageHub:

    @pytest.mark.asyncio
    async def test_lifecycle(self, redis_test_mock_async: aioredis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        hub = eha.AsyncMessageHub(
            redis=redis_test_mock_async,
            name="test",
            packer=ecm.PicklePacker(),
            max_buffer_size=max_buffer_size,
            max_history_size=max_history_size,
        )

        await hub.clear_buffer()
        await hub.clear_history()

        data_size = max_buffer_size
        datas = []
        for idx in range(data_size):
            datas.append({'idx': idx, 'data': f"data-{idx}"})
        reversed_datas = datas[::-1]

        # Push all messages
        for data in datas:
            await hub.push(data)

        assert await hub.history_size() == data_size
        assert await hub.buffer_size() == max_buffer_size

        for idx in range(data_size):
            assert await hub.last(idx) == reversed_datas[idx]

        assert await hub.last_multiple(0, data_size) == reversed_datas

        for idx in range(data_size):
            assert await hub.pop() == datas[idx]

        assert await hub.history_size() == data_size
        assert await hub.buffer_size() == 0

        await hub.clear_history()
        assert await hub.history_size() == 0

        # Push all messages
        for data in datas:
            await hub.push(data)

        await hub.clear_buffer()
        assert await hub.buffer_size() == 0
        assert await hub.pop(1) is None

        assert await hub.last(data_size) is None

        await hub.clear_history()
        await hub.clear_buffer()

        # Push double the messages and pop them
        for data in datas:
            await hub.push(data)
            await hub.push(data)

        assert await hub.history_size() == data_size
        assert await hub.buffer_size() == data_size

        await hub.clear_buffer()
        await hub.clear_history()

    @pytest.mark.asyncio
    async def test_max_payload(self, redis_test_mock_async: aioredis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size
        max_payload_size = 1_000_000

        hub = eha.AsyncMessageHub(
            redis=redis_test_mock_async,
            name="test",
            packer=ecm.PicklePacker(),
            max_buffer_size=max_buffer_size,
            max_history_size=max_history_size,
            max_payload_size=max_payload_size,
        )

        await hub.clear_buffer()
        await hub.clear_history()

        data = [b'0' * max_payload_size * 2]

        with pytest.raises(ValueError):
            await hub.push(data)

        await hub.clear_buffer()
        await hub.clear_history()

    @pytest.mark.asyncio
    async def test_factory(self):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        hub = eha.AsyncMessageHub.create(
            "test",
            config=eh.HubsConfig(
                redis_host="fakeredis",
                max_buffer_size=max_buffer_size,
                max_history_size=max_history_size,
            ),
        )

        await hub.clear_buffer()
        await hub.clear_history()

        data = [b'0']
        for _ in range(max_buffer_size):
            await hub.push(data)

        assert await hub.buffer_size() == max_buffer_size

        await hub.clear_buffer()
        await hub.clear_history()
