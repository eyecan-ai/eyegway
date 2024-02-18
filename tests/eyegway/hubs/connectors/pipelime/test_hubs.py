import eyegway.hubs as eh
import eyegway.hubs.asyn as eha
import eyegway.hubs.sync as ehs
import eyegway.hubs.connectors.pipelime as ehcp
import pytest
import pathlib as pl
import pipelime.sequences as pls
import pipelime.items as pli
import typing as t


## Valid Dataset contains items supported by the default connector
@pytest.fixture
def valid_dataset_folder() -> pl.Path:
    return pl.Path(__file__).parent / "dataset_valid"


# ## Invalid Dataset contains extra items not supported by the default connector
# @pytest.fixture
# def invalid_dataset_folder() -> pl.Path:
#     return pl.Path(__file__).parent / "dataset_invalid"


class TestPipelimeConnector:

    @pytest.mark.asyncio
    async def test_async_valid(self, valid_dataset_folder: pl.Path):

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

        dataset = pls.SamplesSequence.from_underfolder(valid_dataset_folder)

        assert len(dataset) > 0

        for sample in dataset:
            await hub.push(sample)

            assert await hub.buffer_size() == 1

            resample = await hub.pop()
            assert isinstance(resample, pls.Sample)

            print("KEYS", list(sample.keys()), list(resample.keys()))
            assert set(sample.keys()) == set(resample.keys())

    def test_sync_valid(self, valid_dataset_folder: pl.Path):

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

        hub.connectors.append(ehcp.PipelimeHubConnector())

        hub.clear_buffer()
        hub.clear_history()

        dataset = pls.SamplesSequence.from_underfolder(valid_dataset_folder)

        assert len(dataset) > 0

        for sample in dataset:
            hub.push(sample)

            assert hub.buffer_size() == 1

            resample = hub.pop()
            assert isinstance(resample, pls.Sample)

            print("KEYS", list(sample.keys()), list(resample.keys()))
            assert set(sample.keys()) == set(resample.keys())
