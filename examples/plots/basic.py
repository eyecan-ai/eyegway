import math
import random
import threading
import time
from pathlib import Path
from typing import Any, Dict

from rich import print

from eyegway.hubs.sync import MessageHub
from eyegway.hubs.viewers.keys import KeysView
from eyegway.utils.plotting import Dashboard, Plot

##########################
# SAMPLE DATA GENERATORS #
##########################

start_time = time.time()


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
        return {
            "x": time.time() - start_time,
            "y": self.current_value,
        }


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
        return {
            "x": time.time() - start_time,
            "y": value,
        }


class HelixGenerator(DataGenerator):
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
        return {
            "x": time.time() - start_time,
            "y": value_y,
            "z": value_z,
            "marker": {"color": time.time() - start_time},
        }


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
        return {
            "x": time.time() - start_time,
            "y": value,
            "marker": {"color": time.time() - start_time},
        }


if __name__ == "__main__":

    ###############
    # HUBS CONFIG #
    ###############
    rand_hub = MessageHub.create("random_walk")
    sine_hub = MessageHub.create("sine")
    helix_hub = MessageHub.create("helix")
    daily_hub = MessageHub.create("daily_production")
    plt_hub = MessageHub.create("plot_hub")

    # Clear all hubs
    rand_hub.clear()
    sine_hub.clear()
    helix_hub.clear()
    daily_hub.clear()
    plt_hub.clear()

    ##########################
    # SAMPLE DATA GENERATORS #
    ##########################

    random_walk_generator = RandomWalkGenerator("random_walk")
    sine_generator = SineGenerator("sine")
    daily_production_generator = DailyProductionGenerator("daily_production")
    helix_generator = HelixGenerator("helix")

    #######################
    # HUB VIEWER SETTINGS #
    #######################
    rand_hub.viewer = KeysView(keys=["x", "y"])
    sine_hub.viewer = KeysView(keys=["x", "y"])
    daily_hub.viewer = KeysView(keys=["x", "y", "marker.color"])
    helix_hub.viewer = KeysView(keys=["x", "y", "z", "marker.color"])

    ######################
    # PLOT CONFIGURATION #
    ######################

    rand_plt = Plot.from_file("Random Walk", Path("basic_plots/chart_red.json"))
    sine_plt = Plot.from_file("Sine Wave", Path("basic_plots/chart_blue.json"))
    helix_plt = Plot.from_file("Helix", Path("basic_plots/3d_scatter.json"))
    daily_plt = Plot.from_file("Daily Prod", Path("basic_plots/bar_colors.json"))

    ##################
    # LAUNCH THREADS #
    ##################

    generators = [
        threading.Thread(target=random_walk_generator.run, daemon=True),
        threading.Thread(target=sine_generator.run, daemon=True),
        threading.Thread(target=helix_generator.run, daemon=True),
        threading.Thread(target=daily_production_generator.run, daemon=True),
    ]

    for t in generators:
        t.start()

    dashboard = Dashboard(
        [rand_hub, sine_hub, daily_hub, helix_hub],
        [rand_plt, sine_plt, daily_plt, helix_plt],
        plt_hub,
    )

    dash_thread = threading.Thread(target=dashboard.run, daemon=True)
    dash_thread.start()

    print(
        "Data generation and plot updating started...\n"
        f"Plot names: [yellow]{rand_plt.name}[/yellow], "
        f"[yellow]{sine_plt.name}[/yellow], [yellow]{daily_plt.name}[/yellow], "
        f"[yellow]{helix_plt.name}[/yellow]\n"
        "[red]Press Ctrl+C to stop the data generation and plot updating[/red]"
    )

    try:
        dash_thread.join()
        for t in generators:
            t.join()
    except KeyboardInterrupt:
        print("Stopped all threads")
