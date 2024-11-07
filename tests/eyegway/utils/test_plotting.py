import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.sync import MessageHub
from eyegway.hubs.viewers import ValueAccumulatorView
from eyegway.utils.plotting import Dashboard, Plot


class TestPlot:

    def test_plot_initialization(self):
        plot = Plot(name="test_plot")
        assert plot.name == "test_plot"
        assert plot.data == []
        assert plot.layout == {}
        assert plot.config == {}

    def test_plot_from_file(self, tmp_path):
        params = {
            "data": [{"x": [1, 2, 3], "y": [4, 5, 6]}],
            "layout": {"title": "Test Plot"},
            "config": {"responsive": True},
        }
        params_path = tmp_path / "params.json"
        with open(params_path, "w") as f:
            json.dump(params, f)

        plot = Plot.from_file(name="test_plot", params_path=params_path)
        assert plot.name == "test_plot"
        assert plot.data == params["data"]
        assert plot.layout == params["layout"]
        assert plot.config == params["config"]

    def test_plot_from_dict(self):
        params = {
            "data": [{"x": [1, 2, 3], "y": [4, 5, 6]}],
            "layout": {"title": "Test Plot"},
            "config": {"responsive": True},
        }
        plot = Plot.from_dict(name="test_plot", params=params)
        assert plot.name == "test_plot"
        assert plot.data == params["data"]
        assert plot.layout == params["layout"]
        assert plot.config == params["config"]

    def test_plot_pack(self):
        plot = Plot(name="test_plot", data=[{"x": [1, 2, 3], "y": [4, 5, 6]}])
        packed_data = plot.pack()
        assert packed_data == {
            "test_plot": {
                "data": [{"x": [1, 2, 3], "y": [4, 5, 6]}],
                "layout": {},
                "config": {},
            }
        }

    def test_plot_update(self):
        plot = Plot(name="test_plot", data=[{"x": [1, 2, 3], "y": [4, 5, 6]}])
        new_params = {
            "data": [{"x": [1, 2, 3], "y": [7, 8, 9]}],
            "layout": {"title": "Updated Plot"},
            "config": {"responsive": False},
        }
        plot.update(new_params)
        assert plot.data[0]["y"] == [7, 8, 9]
        assert plot.layout["title"] == "Updated Plot"
        assert plot.config["responsive"] is False


class TestDashboard:

    def test_dashboard_initialization(self):
        source_hubs = [MagicMock(spec=MessageHub), MagicMock(spec=MessageHub)]
        viewers = ValueAccumulatorView(keys=["x", "y"])
        plots = [Plot(name="plot1"), Plot(name="plot2")]
        target_hub = MagicMock(spec=MessageHub)
        dashboard = Dashboard(source_hubs, viewers, plots, target_hub)
        assert dashboard.source_hubs == source_hubs
        assert dashboard.plots == plots
        assert dashboard.target_hub == target_hub

        with pytest.raises(ValueError):
            Dashboard(source_hubs, [viewers], plots, target_hub)

    def test_dashboard_initialization_mismatch(self):
        source_hubs = [MagicMock(spec=MessageHub)]
        plots = [Plot(name="plot1"), Plot(name="plot2")]
        viewers = ValueAccumulatorView(keys=["x", "y"])
        target_hub = MagicMock(spec=MessageHub)
        with pytest.raises(ValueError):
            Dashboard(source_hubs, viewers, plots, target_hub)

    def test_dashboard_run_sync(self):
        source_hubs = [MagicMock(spec=MessageHub), MagicMock(spec=MessageHub)]
        plots = [Plot(name="plot1"), Plot(name="plot2")]
        viewers = [
            ValueAccumulatorView(keys=["x", "y"]),
            ValueAccumulatorView(keys=["x", "y"]),
        ]
        target_hub = MagicMock(spec=MessageHub)
        dashboard = Dashboard(source_hubs, viewers, plots, target_hub)

        with patch("time.sleep", return_value=None) as mock_sleep:
            mock_sleep.side_effect = [None, None, KeyboardInterrupt]
            dashboard.run_sync()

        assert target_hub.push.called
        assert target_hub.push.call_count == 3

        # We test ValueErrors if source_hubs or target_hub are not of the correct type
        source_hubs = [MagicMock(spec=AsyncMessageHub)]
        plots = [Plot(name="plot1")]
        viewers = [ValueAccumulatorView(keys=["x", "y"])]
        target_hub = MagicMock(spec=MessageHub)
        dashboard = Dashboard(source_hubs, viewers, plots, target_hub)

        with pytest.raises(ValueError):
            dashboard.run_sync()

        source_hubs = [MagicMock(spec=MessageHub)]
        plots = [Plot(name="plot1")]
        viewers = [ValueAccumulatorView(keys=["x", "y"])]
        target_hub = MagicMock(spec=AsyncMessageHub)
        dashboard = Dashboard(source_hubs, viewers, plots, target_hub)

        with pytest.raises(ValueError):
            dashboard.run_sync()

    @pytest.mark.asyncio
    async def test_dashboard_run_async(self):
        source_hubs = [
            AsyncMock(spec=AsyncMessageHub),
            AsyncMock(spec=AsyncMessageHub),
            MagicMock(spec=MessageHub),
        ]
        plots = [
            Plot(name="plot1", data=[{"x": [0], "y": [0], "marker": {"color": 0}}]),
            Plot(name="plot2", data=[{"x": [0], "y": [0], "marker": {"color": 0}}]),
            Plot(name="plot3", data=[{"x": [0], "y": [0]}]),
        ]
        viewers = [
            ValueAccumulatorView(keys=["x", "y"]),
            ValueAccumulatorView(keys=["x", "y", "marker.color"]),
            ValueAccumulatorView(keys=["x", "y"]),
        ]

        target_hub_async = AsyncMock(spec=AsyncMessageHub)
        dashboard_to_sync = Dashboard(source_hubs, viewers, plots, target_hub_async)

        target_hub_sync = MagicMock(spec=MessageHub)
        dashboard_to_async = Dashboard(source_hubs, viewers, plots, target_hub_sync)

        task_to_sync = asyncio.create_task(dashboard_to_sync.run_async())
        task_to_async = asyncio.create_task(dashboard_to_async.run_async())

        await asyncio.sleep(0.1)

        task_to_sync.cancel()
        try:
            await task_to_sync
        except asyncio.CancelledError:
            pass

        task_to_async.cancel()
        try:
            await task_to_async
        except asyncio.CancelledError:
            pass

        assert target_hub_async.push.called
        assert target_hub_async.push.call_count > 0

        assert target_hub_sync.push.called
        assert target_hub_sync.push.call_count > 0
