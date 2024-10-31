import asyncio
from unittest.mock import patch

import numpy as np
import pytest

import eyegway.hubs.asyn as eha
import eyegway.hubs.sync as ehs
import eyegway.packers as ecm
import eyegway.utils.generators as eug


class TestDemoData:

    def test_random_walk_generator(self):
        generator = eug.RandomWalkGenerator()
        data = generator.generate()
        assert isinstance(data, dict)
        assert "x" in data
        assert "y" in data
        assert isinstance(data["x"], float)
        assert isinstance(data["y"], float)

    def test_sine_generator(self):
        generator = eug.SineGenerator()
        data = generator.generate()
        assert isinstance(data, dict)
        assert "x" in data
        assert "y" in data
        assert isinstance(data["x"], float)
        assert isinstance(data["y"], float)
        assert -1 <= data["y"] <= 1

    def test_helix_generator(self):
        generator = eug.HelixGenerator()
        data = generator.generate()
        assert isinstance(data, dict)
        assert "x" in data
        assert "y" in data
        assert "z" in data
        assert "marker" in data
        assert isinstance(data["x"], float)
        assert isinstance(data["y"], float)
        assert isinstance(data["z"], float)
        assert isinstance(data["marker"], dict)
        assert "color" in data["marker"]
        assert isinstance(data["marker"]["color"], float)
        assert -1 <= data["y"] <= 1
        assert -1 <= data["z"] <= 1

    def test_daily_production_generator(self):
        generator = eug.DailyProductionGenerator()
        data = generator.generate()
        assert isinstance(data, dict)
        assert "x" in data
        assert "y" in data
        assert "marker" in data
        assert isinstance(data["x"], float)
        assert isinstance(data["y"], float)
        assert isinstance(data["marker"], dict)
        assert "color" in data["marker"]
        assert isinstance(data["marker"]["color"], float)
        assert generator.min_value <= data["y"] <= generator.max_value

    def test_demo_data_generator(self):
        generator = eug.DemoDataGenerator()
        data = generator.generate()
        assert isinstance(data, dict)
        expected_keys = [
            "image_0",
            "image_1",
            "image_2",
            "image_counter_squared",
            "image_counter_letterbox",
            "image_counter_pillarbox",
            "metadata",
            "counter",
        ]
        for key in expected_keys:
            assert key in data
        image_keys = expected_keys[:-2]
        for key in image_keys:
            assert isinstance(data[key], np.ndarray)
        assert isinstance(data["metadata"], dict)
        metadata_keys = ["timestamp", "author", "description", "counter"]
        for key in metadata_keys:
            assert key in data["metadata"]
        assert isinstance(data["counter"], int)


class MockGenerator(eug.DataGenerator):
    def generate(self):
        return {"data": "test"}


def test_data_pusher_sync(redis_test_mock_sync):
    max_buffer_size = 10
    max_history_size = max_buffer_size

    hub = ehs.MessageHub(
        redis=redis_test_mock_sync,
        name="test_sync_interrupt",
        packer=ecm.PicklePacker(),
        max_buffer_size=max_buffer_size,
        max_history_size=max_history_size,
    )

    hub.clear_buffer()
    hub.clear_history()

    generator = MockGenerator()
    data_pusher = eug.DataPusher(generator, hub, interval=0.1)

    with patch("time.sleep", return_value=None) as mock_sleep:

        mock_sleep.side_effect = [None, None, KeyboardInterrupt]

        data_pusher.run_sync()

    buffer_size = hub.buffer_size()
    assert buffer_size == 3


@pytest.mark.asyncio
async def test_data_pusher_async(redis_test_mock_async):
    max_buffer_size = 10
    max_history_size = max_buffer_size

    hub = eha.AsyncMessageHub(
        redis=redis_test_mock_async,
        name="test_async_interrupt",
        packer=ecm.PicklePacker(),
        max_buffer_size=max_buffer_size,
        max_history_size=max_history_size,
    )

    await hub.clear_buffer()
    await hub.clear_history()

    generator = MockGenerator()
    data_pusher = eug.DataPusher(generator, hub, interval=0.1)

    task = asyncio.create_task(data_pusher.run_async())

    await asyncio.sleep(0.1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    buffer_length = await hub.buffer_size()
    assert buffer_length > 0
