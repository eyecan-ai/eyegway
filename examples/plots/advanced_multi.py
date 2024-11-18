import threading
import time
from pathlib import Path

from rich import print

import eyegway.utils.generators as eug
from eyegway.hubs.sync import MessageHub
from eyegway.hubs.viewers import ValueAccumulatorView
from eyegway.utils.plotting import Plot

if __name__ == "__main__":

    ###############
    # HUBS CONFIG #
    ###############
    rand_hub = MessageHub.create("random_walk")
    sine_hub = MessageHub.create("sine")
    bar_hub = MessageHub.create("bar_hub")
    helix_hub = MessageHub.create("helix")
    plt_hub = MessageHub.create("plot_hub")

    # Clear all hubs
    rand_hub.clear()
    sine_hub.clear()
    helix_hub.clear()
    bar_hub.clear()
    plt_hub.clear()

    ##################
    # VIEWERS CONFIG #
    ##################
    rand_viewer = ValueAccumulatorView(keys=["x", "y"])
    sine_viewer = ValueAccumulatorView(keys=["x", "y"])
    bar_viewer = ValueAccumulatorView(keys=["x", "y", "z", "marker.color"])
    helix_viewer = ValueAccumulatorView(keys=["x", "y", "marker.color"])

    ##########################
    # SAMPLE DATA GENERATORS #
    ##########################

    rand_pusher = eug.DataPusher(eug.RandomWalkGenerator(), rand_hub)
    sine_pusher = eug.DataPusher(eug.SineGenerator(), sine_hub)
    bar_pusher = eug.DataPusher(eug.DailyProductionGenerator(), bar_hub)
    helix_pusher = eug.DataPusher(eug.HelixGenerator(), helix_hub)

    ######################
    # PLOT CONFIGURATION #
    ######################

    rand_plt = Plot.from_file(Path("basic_plots/chart_red.json"))
    sine_plt = Plot.from_file(Path("basic_plots/chart_blue.json"))
    bar_plt = Plot.from_file(Path("basic_plots/bar_colors.json"))
    helix_plt = Plot.from_file(Path("basic_plots/3d_scatter.json"))

    ##################
    # LAUNCH THREADS #
    ##################

    generators = [
        threading.Thread(target=rand_pusher.run_sync, daemon=True),
        threading.Thread(target=sine_pusher.run_sync, daemon=True),
        threading.Thread(target=helix_pusher.run_sync, daemon=True),
        threading.Thread(target=bar_pusher.run_sync, daemon=True),
    ]

    for g in generators:
        g.start()

    print(
        "Data generation and plot updating started...\n"
        "Plot names: [yellow]Random Walk[/yellow], "
        "[yellow]Sine Wave[/yellow], [yellow]Bars[/yellow], "
        "[yellow]Helix[/yellow]\n"
        "[red]Press Ctrl+C to stop the data generation and plot updating[/red]"
    )

    while True:
        rand_data = rand_viewer._sync_view(rand_hub)
        sine_data = sine_viewer._sync_view(sine_hub)
        bar_data = bar_viewer._sync_view(bar_hub)
        helix_data = helix_viewer._sync_view(helix_hub)

        rand_plt.update({"data": [{"x": rand_data["x"], "y": rand_data["y"]}]})
        sine_plt.update({"data": [{"x": sine_data["x"], "y": sine_data["y"]}]})
        bar_plt.update(
            {
                "data": [
                    {
                        "x": bar_data["x"],
                        "y": bar_data["y"],
                        "marker": {"color": bar_data["marker.color"]},
                    }
                ]
            }
        )
        helix_plt.update(
            {
                "data": [
                    {
                        "x": helix_data["x"],
                        "y": helix_data["y"],
                        "marker": {"color": helix_data["marker.color"]},
                    }
                ]
            }
        )

        plt_hub.push(
            {
                "Random Walk": rand_plt.to_dict(),
                "Sine Wave": sine_plt.to_dict(),
                "Bars": bar_plt.to_dict(),
                "Helix": helix_plt.to_dict(),
            }
        )
        time.sleep(0.01)
