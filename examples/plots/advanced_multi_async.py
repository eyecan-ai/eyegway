from pathlib import Path

from rich import print

import eyegway.utils.generators as eug
from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.viewers import ValueAccumulatorView
from eyegway.utils.plotting import Dashboard, Plot

if __name__ == "__main__":

    import asyncio

    async def main():

        ###############
        # HUBS CONFIG #
        ###############
        rand_hub = AsyncMessageHub.create("random_walk")
        sine_hub = AsyncMessageHub.create("sine")
        bar_hub = AsyncMessageHub.create("bar_hub")
        helix_hub = AsyncMessageHub.create("helix")
        plt_hub = AsyncMessageHub.create("plot_hub")

        # Clear all hubs
        await rand_hub.clear()
        await sine_hub.clear()
        await helix_hub.clear()
        await bar_hub.clear()
        await plt_hub.clear()

        # Add viewer
        rand_viewer = ValueAccumulatorView(keys=["x", "y"])
        sine_viewer = ValueAccumulatorView(keys=["x", "y"])
        bar_viewer = ValueAccumulatorView(keys=["x", "y", "marker.color"])
        helix_viewer = ValueAccumulatorView(keys=["x", "y", "z", "marker.color"])

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

        rand_plt = Plot.from_file("Random Walk", Path("basic_plots/chart_red.json"))
        sine_plt = Plot.from_file("Sine Wave", Path("basic_plots/chart_blue.json"))
        bar_plt = Plot.from_file("Bars", Path("basic_plots/bar_colors.json"))
        helix_plt = Plot.from_file("Helix", Path("basic_plots/3d_scatter.json"))

        ###########################
        # DASHBOARD CONFIGURATION #
        ###########################
        dashboard = Dashboard(
            [rand_hub, sine_hub, bar_hub, helix_hub],
            [rand_viewer, sine_viewer, bar_viewer, helix_viewer],
            [rand_plt, sine_plt, bar_plt, helix_plt],
            plt_hub,
        )

        ################
        # LAUNCH TASKS #
        ################

        generators = [
            asyncio.create_task(rand_pusher.run_async()),
            asyncio.create_task(sine_pusher.run_async()),
            asyncio.create_task(bar_pusher.run_async()),
            asyncio.create_task(helix_pusher.run_async()),
        ]

        dash_task = asyncio.create_task(dashboard.run_async())

        print(
            "Data generation and plot updating started...\n"
            f"Plot names: [yellow]{rand_plt.name}[/yellow], "
            f"[yellow]{sine_plt.name}[/yellow], [yellow]{bar_plt.name}[/yellow], "
            f"[yellow]{helix_plt.name}[/yellow]\n"
            "[red]Press Ctrl+C to stop the data generation and plot updating[/red]"
        )

        await asyncio.gather(dash_task, *generators)

    asyncio.run(main())
