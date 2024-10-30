import asyncio
import pathlib as pl
import time
import typing as t

from loguru import logger

from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.sync import MessageHub


class Plot:
    """Prepare and update plots with data from hubs."""

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
        import json

        with open(params_path) as f:
            params = dict(json.load(f))
            return cls.from_dict(name=name, params=params)

    @classmethod
    def from_dict(cls, name: str, params: t.Dict) -> "Plot":
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
        self.data = [
            self._merge(o, n) for o, n in zip(self.data, params.get("data", []))
        ]
        self.layout = self._merge(self.layout, params.get("layout", self.layout))
        self.config = self._merge(self.config, params.get("config", self.config))


class Dashboard:
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
        return {
            plot.name: {"data": plot.data, "layout": plot.layout, "config": plot.config}
        }

    def run(self, tick_time: float = 0.1) -> None:
        """Starts the continuous updating of plots."""
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
        return {
            plot.name: {"data": plot.data, "layout": plot.layout, "config": plot.config}
        }

    async def run(self, tick_time: float = 0.1) -> None:
        """Starts the continuous updating of plots."""
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
