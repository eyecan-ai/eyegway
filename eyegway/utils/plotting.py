import asyncio
import pathlib as pl
import time
import typing as t

from loguru import logger

from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.sync import MessageHub


class Plot:
    """
    Prepare and update plots with data from hubs.

    Attributes:
        name (str): The name of the plot.
        data (Optional[List]): The data for the plot.
        layout (Optional[dict]): The layout configuration for the plot.
        config (Optional[dict]): The configuration for the plot.

    Example:
        # Basic example
        plot = Plot(name="example_plot")
        plot.update({"data": [{"x": [1, 2, 3], "y": [4, 5, 6]}]})

        # Example with layout and scatter data
        plot = Plot(
            name="scatter_plot",
            data=[{"type": "scatter", "x": [1, 2, 3], "y": [4, 5, 6]}],
            layout={"title": "Scatter Plot Example"}
        )
        plot.update({"data": [{"x": [1, 2, 3], "y": [4, 5, 6]}]})
    """

    def __init__(
        self,
        name: str,
        data: t.Optional[t.List] = None,
        layout: t.Optional[dict] = None,
        config: t.Optional[dict] = None,
    ):
        if data is None:
            data = []

        if layout is None:
            layout = {}

        if config is None:
            config = {}

        self.name = name
        self.data = data
        self.layout = layout
        self.config = config

    @classmethod
    def from_file(cls, name: str, params_path: pl.Path) -> "Plot":
        """
        Creates a Plot instance from a JSON file.

        Args:
            name (str): The name of the plot.
            params_path (Path): The path to the JSON file containing plot parameters.

        Returns:
            Plot: A new Plot instance.
        """
        import json

        with open(params_path) as f:
            params = dict(json.load(f))
            return cls.from_dict(name=name, params=params)

    @classmethod
    def from_dict(cls, name: str, params: t.Dict) -> "Plot":
        """
        Creates a Plot instance from a dictionary.

        Args:
            name (str): The name of the plot.
            params (Dict): A dictionary containing plot parameters.

        Returns:
            Plot: A new Plot instance.
        """
        return cls(name=name, **params)

    @staticmethod
    def _merge(d1: t.Dict[str, t.Any], d2: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """
        Recursively merges two dictionaries.
        If there are nested dictionaries, they are merged as well.

        Args:
            d1 (dict): The first dictionary.
            d2 (dict): The second dictionary.

        Returns:
            dict: The merged dictionary.
        """
        for key, value in d2.items():
            if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                d1[key] = Plot._merge(d1[key], value)
            else:
                d1[key] = value
        return d1

    def update(self, params: t.Dict) -> None:
        """
        Updates the plot with new parameters.

        Args:
            params (Dict): A dictionary containing new plot parameters.
        """
        self.data = [
            self._merge(o, n) for o, n in zip(self.data, params.get("data", []))
        ]
        self.layout = self._merge(self.layout, params.get("layout", self.layout))
        self.config = self._merge(self.config, params.get("config", self.config))


class Dashboard:
    """
    Manages and updates multiple plots with data from synchronous message hubs.

    Attributes:
        source_hubs (List[MessageHub]): A list of source message hubs.
        plots (List[Plot]): A list of plots to be updated.
        target_hub (MessageHub): The target message hub to push updated plots.

    Example:
        source_hubs = [MessageHub(), MessageHub()]
        plots = [Plot(name="plot1"), Plot(name="plot2")]
        target_hub = MessageHub()
        dashboard = Dashboard(source_hubs, plots, target_hub)
        dashboard.run(tick_time=0.1)
    """

    def __init__(
        self,
        source_hubs: t.List[MessageHub],
        plots: t.List[Plot],
        target_hub: MessageHub,
    ) -> None:
        if len(source_hubs) != len(plots):
            err = "Number of source hubs and plots must match"
            raise ValueError(err)

        self.source_hubs = source_hubs
        self.plots = plots
        self.target_hub = target_hub

    def _pack(self, plot: Plot) -> t.Dict[str, t.Any]:
        """
        Packs the plot data into a dictionary.

        Args:
            plot (Plot): The plot to be packed.

        Returns:
            Dict[str, Any]: A dictionary containing the plot data.
        """
        return {
            plot.name: {"data": plot.data, "layout": plot.layout, "config": plot.config}
        }

    def run(self, tick_time: float = 0.1) -> None:
        """
        Starts the continuous updating of plots.

        Args:
            tick_time (float): The time interval between updates in seconds.
        """
        try:
            while True:
                for plot, hub in zip(self.plots, self.source_hubs):
                    data = hub.view()
                    plot.update({"data": [data]})  # TODO: Check this list
                plots_data = {}
                for plot in self.plots:
                    plots_data.update(self._pack(plot))
                self.target_hub.push(plots_data)
                time.sleep(tick_time)
        except KeyboardInterrupt:
            logger.info("Stopped plot updating")


class AsyncDashboard:
    """
    Manages and updates multiple plots with data from asynchronous message hubs.

    Attributes:
        source_hubs (List[AsyncMessageHub]): A list of source asynchronous message hubs.
        plots (List[Plot]): A list of plots to be updated.
        target_hub (AsyncMessageHub): The target asynchronous message hub to
                                        push updated plots.

    Example:
        source_hubs = [AsyncMessageHub(), AsyncMessageHub()]
        plots = [Plot(name="plot1"), Plot(name="plot2")]
        target_hub = AsyncMessageHub()
        dashboard = AsyncDashboard(source_hubs, plots, target_hub)
        asyncio.run(dashboard.run(tick_time=0.1))
    """

    def __init__(
        self,
        source_hubs: t.List[AsyncMessageHub],
        plots: t.List[Plot],
        target_hub: AsyncMessageHub,
    ) -> None:
        if len(source_hubs) != len(plots):
            err = "Number of source hubs and plots must match"
            raise ValueError(err)

        self.source_hubs = source_hubs
        self.plots = plots
        self.target_hub = target_hub

    def _pack(self, plot: Plot) -> t.Dict[str, t.Any]:
        """
        Packs the plot data into a dictionary.

        Args:
            plot (Plot): The plot to be packed.

        Returns:
            Dict[str, Any]: A dictionary containing the plot data.
        """
        return {
            plot.name: {"data": plot.data, "layout": plot.layout, "config": plot.config}
        }

    async def run(self, tick_time: float = 0.1) -> None:
        """
        Starts the continuous updating of plots.

        Args:
            tick_time (float): The time interval between updates in seconds.
        """
        try:
            while True:
                for plot, hub in zip(self.plots, self.source_hubs):
                    data = await hub.view()
                    plot.update({"data": [data]})  # TODO: Check this list
                plots_data = {}
                for plot in self.plots:
                    plots_data.update(self._pack(plot))
                await self.target_hub.push(plots_data)
                await asyncio.sleep(tick_time)
        except KeyboardInterrupt:
            logger.info("Stopped plot updating")
