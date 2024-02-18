import eyegway.hubs as eh
import eyegway.hubs.sync as ehs
import eyegway.packers as ecm
import redis
import pytest
import typing as t


class TestMessageHub:

    def test_lifecycle(self, redis_test_mock_sync: redis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        hub = ehs.MessageHub(
            redis=redis_test_mock_sync,
            name="test",
            packer=ecm.PicklePacker(),
            max_buffer_size=max_buffer_size,
            max_history_size=max_history_size,
        )

        hub.clear_buffer()
        hub.clear_history()

        data_size = max_buffer_size
        datas = []
        for idx in range(data_size):
            datas.append({'idx': idx, 'data': f"data-{idx}"})
        reversed_datas = datas[::-1]

        # Push all messages
        for data in datas:
            hub.push(data)

        assert hub.history_size() == data_size
        assert hub.buffer_size() == max_buffer_size

        for idx in range(data_size):
            assert hub.last(idx) == reversed_datas[idx]

        assert hub.last_multiple(0, data_size) == reversed_datas

        for idx in range(data_size):
            assert hub.pop() == datas[idx]

        assert hub.history_size() == data_size
        assert hub.buffer_size() == 0

        hub.clear_history()
        assert hub.history_size() == 0

        # Push all messages
        for data in datas:
            hub.push(data)

        hub.clear_buffer()
        assert hub.buffer_size() == 0
        assert hub.pop(1) is None

        assert hub.last(data_size) is None

        hub.clear()

        # Push double the messages and pop them
        for data in datas:
            hub.push(data)
            hub.push(data)

        assert hub.history_size() == data_size
        assert hub.buffer_size() == data_size

        hub.clear_buffer()
        hub.clear_history()

    def test_max_payload(self, redis_test_mock_sync: redis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size
        max_payload_size = 1_000_000

        hub = ehs.MessageHub(
            redis=redis_test_mock_sync,
            name="test",
            packer=ecm.PicklePacker(),
            max_buffer_size=max_buffer_size,
            max_history_size=max_history_size,
            max_payload_size=max_payload_size,
        )

        hub.clear_buffer()
        hub.clear_history()

        data = [b'0' * max_payload_size * 2]

        with pytest.raises(ValueError):
            hub.push(data)

        hub.clear_buffer()
        hub.clear_history()

    def test_factory_only_creation(self):
        hub = ehs.MessageHub.create("test")

    def test_factory(self):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        hub = ehs.MessageHub.create(
            "test",
            config=eh.HubsConfig(
                redis_host="fakeredis",
                max_buffer_size=max_buffer_size,
                max_history_size=max_history_size,
            ),
        )

        hub.clear_buffer()
        hub.clear_history()

        data = [b'0']
        for _ in range(max_buffer_size):
            hub.push(data)

        assert hub.buffer_size() == max_buffer_size

        hub.clear_buffer()
        hub.clear_history()


class TestMessageHubManager:

    def test_lifecycle(self, redis_test_mock_sync: redis.Redis):

        max_buffer_size = 10
        max_history_size = max_buffer_size

        config = eh.HubsConfig(
            redis_host="fakeredis",
            max_buffer_size=max_buffer_size,
            max_history_size=max_history_size,
        )

        hubs_number = 5
        hubs_names = [f"test-{idx}" for idx in range(hubs_number)]
        hubs: t.Dict[str, ehs.MessageHub] = {}

        for hub_name in hubs_names:
            hub = ehs.MessageHub.create(
                hub_name,
                config=config,
                redis=redis_test_mock_sync,
            )
            hubs[hub_name] = hub
            hub.clear()
            hub.push("data".encode('utf-8'))

        manager = ehs.MessageHubManager.create(config, redis=redis_test_mock_sync)

        assert len(manager.list()) == len(hubs_names)

        for hub_name in hubs_names:
            hubs[hub_name].clear_buffer()

        assert len(manager.list()) == len(hubs_names)

        for hub_name in hubs_names:
            hubs[hub_name].clear_history()

        assert len(manager.list()) == 0

    def test_creation(self):
        hub = ehs.MessageHubManager.create()
