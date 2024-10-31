import threading
from pathlib import Path

from rich import print

import eyegway.utils.generators as eug
from eyegway.hubs.sync import MessageHub
from eyegway.hubs.viewers.keys import ValueAccumulatorView
from eyegway.utils.plotting import Dashboard, Plot

if __name__ == "__main__":

    ###############
    # HUBS CONFIG #
    ###############
    rand_hub = MessageHub.create("random_walk")
    sine_hub = MessageHub.create("sine")
    helix_hub = MessageHub.create("helix")
    bar_hub = MessageHub.create("bar_hub")
    plt_hub = MessageHub.create("plot_hub")

    # Add viewer
    rand_hub.viewer = ValueAccumulatorView(keys=["x", "y"])
    sine_hub.viewer = ValueAccumulatorView(keys=["x", "y"])
    bar_hub.viewer = ValueAccumulatorView(keys=["x", "y", "marker.color"])
    helix_hub.viewer = ValueAccumulatorView(keys=["x", "y", "z", "marker.color"])

    # Clear all hubs
    rand_hub.clear()
    sine_hub.clear()
    helix_hub.clear()
    bar_hub.clear()
    plt_hub.clear()

    ##########################
    # SAMPLE DATA GENERATORS #
    ##########################

    rand_wald_pusher = eug.DataPusher(eug.RandomWalkGenerator(), rand_hub)
    sine_pusher = eug.DataPusher(eug.SineGenerator(), sine_hub)
    bar_pusher = eug.DataPusher(eug.DailyProductionGenerator(), bar_hub)
    helix_pusher = eug.DataPusher(eug.HelixGenerator(), helix_hub)

    ######################
    # PLOT CONFIGURATION #
    ######################

    rand_plt = Plot.from_file("Random Walk", Path("basic_plots/chart_red.json"))
    sine_plt = Plot.from_file("Sine Wave", Path("basic_plots/chart_blue.json"))
    helix_plt = Plot.from_file("Helix", Path("basic_plots/3d_scatter.json"))
    bar_plt = Plot.from_file("Bars", Path("basic_plots/bar_colors.json"))

    ##################
    # LAUNCH THREADS #
    ##################

    generators = [
        threading.Thread(target=rand_wald_pusher.run, daemon=True),
        threading.Thread(target=sine_pusher.run, daemon=True),
        threading.Thread(target=helix_pusher.run, daemon=True),
        threading.Thread(target=bar_pusher.run, daemon=True),
    ]

    for g in generators:
        g.start()

    dashboard = Dashboard(
        [rand_hub, sine_hub, bar_hub, helix_hub],
        [rand_plt, sine_plt, bar_plt, helix_plt],
        plt_hub,
    )

    dash_thread = threading.Thread(target=dashboard.run, daemon=True)
    dash_thread.start()

    print(
        "Data generation and plot updating started...\n"
        f"Plot names: [yellow]{rand_plt.name}[/yellow], "
        f"[yellow]{sine_plt.name}[/yellow], [yellow]{bar_plt.name}[/yellow], "
        f"[yellow]{helix_plt.name}[/yellow]\n"
        "[red]Press Ctrl+C to stop the data generation and plot updating[/red]"
    )

    try:
        dash_thread.join()
        for g in generators:
            g.join()
    except KeyboardInterrupt:
        print("Stopped all threads")
