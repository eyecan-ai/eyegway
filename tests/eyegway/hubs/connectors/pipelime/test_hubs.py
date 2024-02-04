import eyegway.hubs as eh
import eyegway.hubs.asyn as eha
import eyegway.hubs.connectors.pipelime as ehcp
import eyegway.commons as ecm
import redis.asyncio as aioredis
import pytest
import pathlib as pl
import pipelime.sequences as pls


@pytest.fixture
def dataset_folder() -> pl.Path:
    return pl.Path(__file__).parent / "dataset"


class TestPipelimeConnector:

    @pytest.mark.asyncio
    async def test_factory(self, dataset_folder: pl.Path):

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

        hub.connectors.append(ehcp.PipelimeHubConnector())

        await hub.clear_buffer()
        await hub.clear_history()

        dataset = pls.SamplesSequence.from_underfolder(dataset_folder)

        for sample in dataset:
            await hub.push(sample)

            assert await hub.buffer_size() == 1

            resample = await hub.pop()
            assert isinstance(resample, pls.Sample)

            print("KEYS", list(sample.keys()), list(resample.keys()))
            assert set(sample.keys()) == set(resample.keys())
