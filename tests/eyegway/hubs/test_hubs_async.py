import eyegway.hubs as eh
import eyegway.hubs.asyn as eha
import eyegway.packers as ecm
import redis.asyncio as aioredis
import pytest
import typing as t


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

        await hub.clear()

        # Push double the messages and pop them
        for data in datas:
            await hub.push(data)
            await hub.push(data)

        assert await hub.history_size() == data_size
        assert await hub.buffer_size() == data_size

        await hub.clear_buffer()
        await hub.clear_history()

    @pytest.mark.asyncio
    async def test_freeze(self, redis_test_mock_async: aioredis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        def _hub():
            return eha.AsyncMessageHub(
                redis=redis_test_mock_async,
                name="test",
                packer=ecm.PicklePacker(),
                max_buffer_size=max_buffer_size,
                max_history_size=max_history_size,
            )

        async def _clear_and_push(hub: eha.AsyncMessageHub):
            await hub.clear_buffer()
            await hub.clear_history()
            data_size = max_buffer_size
            datas = []
            for idx in range(data_size):
                datas.append({'idx': idx, 'data': f"data-{idx}"})

            # Push all messages
            for data in datas:
                await hub.push(data)

        await _hub().freeze_history()
        await _clear_and_push(_hub())

        assert await _hub().history_size() == 0
        assert await _hub().buffer_size() == max_buffer_size

        await _hub().freeze_history(False)
        await _clear_and_push(_hub())

        assert await _hub().history_size() == max_buffer_size
        assert await _hub().buffer_size() == max_buffer_size

        await _hub().freeze_buffer()
        await _clear_and_push(_hub())

        assert await _hub().history_size() == max_buffer_size
        assert await _hub().buffer_size() == 0

        await _hub().freeze_buffer(False)
        await _clear_and_push(_hub())

        assert await _hub().history_size() == max_buffer_size
        assert await _hub().buffer_size() == max_buffer_size

        await _hub().freeze()
        await _clear_and_push(_hub())

        assert await _hub().history_size() == 0
        assert await _hub().buffer_size() == 0

        await _hub().freeze(False)
        await _clear_and_push(_hub())

        assert await _hub().history_size() == max_buffer_size
        assert await _hub().buffer_size() == max_buffer_size

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
    async def test_variables(self, redis_test_mock_async: aioredis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        # create hub each time to avoid variables conflicts
        def _hub():
            return eha.AsyncMessageHub(
                redis=redis_test_mock_async,
                name="test",
                packer=ecm.PicklePacker(),
                max_buffer_size=max_buffer_size,
                max_history_size=max_history_size,
            )

        assert len(await _hub().list_variables()) == 0

        variables = {'alpha': 1, 'beta': False, 'gamma': 3.14}
        for key, value in variables.items():
            assert await _hub().get_variable_value(key) is None

        for key, value in variables.items():
            await _hub().set_variable_value(key, value)

        # test fixed hub to avoid side effects
        hub = _hub()
        for key, value in variables.items():
            await hub.set_variable_value(key, value)
            await hub.set_variable_value(key, value)
            await hub.get_variable_value(key)
            await hub.get_variable_value(key)
        #######################################

        assert len(await _hub().list_variables()) == len(variables)

        for key in variables.keys():
            assert await _hub().get_variable_value(key) == variables[key]

        assert len(await _hub().list_variables()) == len(variables)

        for key in variables.keys():
            assert await _hub().get_variable_value(key) == variables[key]

        for key in variables.keys():
            await _hub().delete_variable(key)

        for key in variables.keys():
            assert await _hub().get_variable_value(key) is None

    @pytest.mark.asyncio
    async def test_factory_only_creation(self):
        hub = eha.AsyncMessageHub.create("test")

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


class TestMessageHubManager:

    @pytest.mark.asyncio
    async def test_lifecycle(self, redis_test_mock_async: aioredis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        config = eh.HubsConfig(
            redis_host="fakeredis",
            max_buffer_size=max_buffer_size,
            max_history_size=max_history_size,
        )

        hubs_number = 5
        hubs_names = [f"test-{idx}" for idx in range(hubs_number)]
        hubs: t.Dict[str, eha.AsyncMessageHub] = {}

        for hub_name in hubs_names:
            hub = eha.AsyncMessageHub.create(
                hub_name,
                config=config,
                redis=redis_test_mock_async,
            )
            await hub.freeze(False)
            hubs[hub_name] = hub
            await hub.clear()
            await hub.push("data".encode('utf-8'))

        manager = eha.AsyncMessageHubManager.create(config, redis=redis_test_mock_async)

        assert len(await manager.list()) == len(hubs_names)

        for hub_name in hubs_names:
            await hubs[hub_name].clear_buffer()

        assert len(await manager.list()) == len(hubs_names)

        for hub_name in hubs_names:
            await hubs[hub_name].clear_history()

        assert len(await manager.list()) == 0

    def test_creation(self):
        hub = eha.AsyncMessageHubManager.create()
