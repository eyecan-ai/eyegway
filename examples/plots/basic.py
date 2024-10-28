import math
import random
import threading
import time
from collections import deque
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Union

from rich import print

from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.sync import MessageHub

##########################
# SAMPLE DATA GENERATORS #
##########################


class DataGenerator:
    """
    Base class for data generators.
    Generates data and pushes it to a message hub at regular intervals.
    """

    def __init__(self, hub_name: str) -> None:
        """
        Initialize the data generator.

        Args:
            hub_name (str): The name of the message hub to push data to.
        """
        self.hub = MessageHub.create(hub_name)
        self.hub_name = hub_name

    def generate_data(self) -> Dict[str, Any]:
        """
        Generate data to be pushed to the hub.

        Returns:
            Dict[str, Any]: The generated data.
        """
        err = "Subclasses should implement this method"
        raise NotImplementedError(err)

    def run(self) -> None:
        """
        Start the data generation loop.
        """
        try:
            while True:
                data = self.generate_data()
                self.hub.push(data)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print(f"Stopped data generation for {self.hub_name}")


class RandomWalkGenerator(DataGenerator):
    """
    Data generator for simulating a random walk.
    """

    def __init__(self, hub_name: str) -> None:
        super().__init__(hub_name)
        self.current_value: float = 0.0

    def generate_data(self) -> Dict[str, Any]:
        """
        Generate the next value in the random walk.

        Returns:
            Dict[str, Any]: The generated data point.
        """
        self.current_value += random.uniform(-1, 1)  # noqa: S311
        return {"x": time.time(), "y": self.current_value}


class SineGenerator(DataGenerator):
    """
    Data generator for simulating a sine wave.
    """

    def __init__(self, hub_name: str) -> None:
        super().__init__(hub_name)
        self.time_step: float = 0.0

    def generate_data(self) -> Dict[str, Any]:
        """
        Generate the next value in the sine wave.

        Returns:
            Dict[str, Any]: The generated data point.
        """
        self.time_step += 0.1
        value = math.sin(self.time_step)
        return {"x": time.time(), "y": value}


class Sine3DGenerator(DataGenerator):
    """
    Data generator for simulating a sine wave.
    """

    def __init__(self, hub_name: str) -> None:
        super().__init__(hub_name)
        self.time_step: float = 0.0

    def generate_data(self) -> Dict[str, Any]:
        """
        Generate the next value in the sine wave.

        Returns:
            Dict[str, Any]: The generated data point.
        """
        self.time_step += 0.1
        value_y = math.sin(self.time_step)
        value_z = math.cos(self.time_step)
        return {"x": time.time(), "y": value_y, "z": value_z}


class DailyProductionGenerator(DataGenerator):
    """
    Data generator for simulating daily production data.
    """

    def __init__(self, hub_name: str) -> None:
        super().__init__(hub_name)

    def generate_data(self) -> Dict[str, Any]:
        """
        Generate a random production value.

        Returns:
            Dict[str, Any]: The generated data point.
        """
        value = random.uniform(80, 120)  # noqa: S311
        return {"x": time.time(), "y": value}


###################
# HUB ACCUMULATOR #
###################


class HubAccumulator:
    """
    Accumulates raw data from hubs and merges data with the same keys into lists.
    """

    def __init__(self, keys: List[str], max_length: Optional[int] = None):
        self.data: Dict[str, Deque[Any]] = {
            key: deque(maxlen=max_length) for key in keys
        }

    def add(self, raw_data: Dict[str, Any]) -> None:
        for key, value in raw_data.items():
            if key in self.data:
                self.data[key].append(value)

    def get_accumulated_data(self) -> Dict[str, List[Any]]:
        return {key: list(values) for key, values in self.data.items()}


###########
# PLOTTER #
###########


class Plotter:
    """Prepare and update plots with data from hubs."""

    def __init__(
        self,
        name: str,
        data: Optional[List] = None,
        layout: Optional[dict] = None,
        config: Optional[dict] = None,
    ):
        if data is None:
            data = []

        if layout is None:
            layout = {}

        if config is None:
            config = {}

        self.name = name
        self._data = data
        self._layout = layout
        self._config = config

    @classmethod
    def from_file(cls, name: str, params_path: Path) -> "Plotter":
        import json

        with open(params_path) as f:
            params = dict(json.load(f))
            return cls.from_dict(name=name, params=params)

    @classmethod
    def from_dict(cls, name: str, params: dict) -> "Plotter":
        return cls(name=name, **params)

    def update(self, params: dict) -> None:
        self._data = [{**o, **n} for o, n in zip(self._data, params.get("data", []))]
        self._layout = {**self._layout, **params.get("layout", self._layout)}
        self._config = {**self._config, **params.get("config", self._config)}

    def pack(self) -> Dict[str, Any]:
        return {
            self.name: {
                "data": self._data,
                "layout": self._layout,
                "config": self._config,
            }
        }


class PlotUpdater:
    """
    Continuously updates multiple plots by:
    1. Fetching data from various hubs,
    2. Accumulating the data,
    3. Pushing the updated plots to the plot hub.
    """

    def __init__(
        self,
        hubs: List[Union[MessageHub, AsyncMessageHub]],
        accumulators: List[HubAccumulator],
        plotters: List[Plotter],
        plot_hub: Union[MessageHub, AsyncMessageHub],
    ):
        """
        Initializes the PlotUpdater with hubs, accumulators, plotters, and the plot hub.

        Args:
            hubs (List[Hub]): Data hubs to fetch data from.
            accumulators (List[HubAccumulator]): Accumulators for each hub.
            plotters (List[Plotter]): Plotters for each hub.
            plot_hub (Hub): Central plot hub where updated plots are pushed.
        """
        self.hubs = hubs
        self.accumulators = accumulators
        self.plotters = plotters
        self.plot_hub = plot_hub

    def update_data(self, data: Any, accumulator: HubAccumulator, plotter: Plotter):
        if data:
            accumulator.add(data)
            plotter.update({"data": [accumulator.get_accumulated_data()]})

    def run(self):
        """Starts the continuous updating of plots."""
        try:
            while True:
                for hub, accumulator, plotter in zip(
                    self.hubs, self.accumulators, self.plotters
                ):
                    data = hub.pop()
                    self.update_data(data, accumulator, plotter)
                updated_plots = {}
                for plotter in self.plotters:
                    updated_plots.update(plotter.pack())
                self.plot_hub.push(updated_plots)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopped plot updating")


if __name__ == "__main__":

    ###############
    # HUBS CONFIG #
    ###############
    rand_hub = MessageHub.create("random_walk")
    sine_hub = MessageHub.create("sine")
    sine3d_hub = MessageHub.create("sine3d")
    daily_hub = MessageHub.create("daily_production")
    plt_hub = MessageHub.create("plot_hub")

    ##########################
    # SAMPLE DATA GENERATORS #
    ##########################

    random_walk_generator = RandomWalkGenerator("random_walk")
    sine_generator = SineGenerator("sine")
    daily_production_generator = DailyProductionGenerator("daily_production")
    sine3d_generator = Sine3DGenerator("sine3d")

    ##########################
    # HUB ACCUMULATOR CONFIG #
    ##########################

    rand_acc = HubAccumulator(keys=["x", "y"], max_length=100)
    sine_acc = HubAccumulator(keys=["x", "y"], max_length=100)
    sine3d_acc = HubAccumulator(keys=["x", "y", "z"], max_length=100)
    daily_acc = HubAccumulator(keys=["x", "y"], max_length=100)

    ######################
    # PLOT CONFIGURATION #
    ######################

    rand_plt = Plotter.from_file("Random Walk", Path("basic_plots/chart_red.json"))
    sine_plt = Plotter.from_file("Sine Wave", Path("basic_plots/chart_blue.json"))
    sine3d_plt = Plotter.from_file("Sine 3D Wave", Path("basic_plots/3d_scatter.json"))
    daily_plt = Plotter.from_file("Daily Prod", Path("basic_plots/bar_colors.json"))

    generators = [
        threading.Thread(target=random_walk_generator.run, daemon=True),
        threading.Thread(target=sine_generator.run, daemon=True),
        threading.Thread(target=sine3d_generator.run, daemon=True),
        threading.Thread(target=daily_production_generator.run, daemon=True),
    ]

    ##################
    # LAUNCH THREADS #
    ##################

    for t in generators:
        t.start()

    plot_updater = PlotUpdater(
        hubs=[rand_hub, sine_hub, daily_hub, sine3d_hub],
        accumulators=[rand_acc, sine_acc, daily_acc, sine3d_acc],
        plotters=[rand_plt, sine_plt, daily_plt, sine3d_plt],
        plot_hub=plt_hub,
    )

    plot_thread = threading.Thread(target=plot_updater.run, daemon=True)
    plot_thread.start()

    print(
        "Data generation and plot updating started...\n"
        f"Plot names: [yellow]{rand_plt.name}[/yellow], "
        f"[yellow]{sine_plt.name}[/yellow], [yellow]{daily_plt.name}[/yellow], "
        f"[yellow]{sine3d_plt.name}[/yellow] (<-- not working right now!)\n"
        "[red]Press Ctrl+C to stop the data generation and plot updating[/red]"
    )

    try:
        plot_thread.join()
        for t in generators:
            t.join()
    except KeyboardInterrupt:
        print("Stopped all threads")
