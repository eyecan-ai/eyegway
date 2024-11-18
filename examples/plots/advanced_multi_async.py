from pathlib import Path

from rich import print

import eyegway.utils.generators as eug
from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.viewers import ValueAccumulatorView
from eyegway.utils.plotting import Plot

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

        rand_plt = Plot.from_file(Path("basic_plots/chart_red.json"))
        sine_plt = Plot.from_file(Path("basic_plots/chart_blue.json"))
        bar_plt = Plot.from_file(Path("basic_plots/bar_colors.json"))
        helix_plt = Plot.from_file(Path("basic_plots/3d_scatter.json"))

        ################
        # LAUNCH TASKS #
        ################

        generators = [
            asyncio.create_task(rand_pusher.run_async()),
            asyncio.create_task(sine_pusher.run_async()),
            asyncio.create_task(bar_pusher.run_async()),
            asyncio.create_task(helix_pusher.run_async()),
        ]

        print(
            "Data generation and plot updating started...\n"
            "Plot names: [yellow]Random Walk[/yellow], "
            "[yellow]Sine Wave[/yellow], [yellow]Bars[/yellow], "
            "[yellow]Helix[/yellow]\n"
            "[red]Press Ctrl+C to stop the data generation and plot updating[/red]"
        )

        await asyncio.gather(*generators)

        while True:
            rand_data = await rand_viewer.view(rand_hub)
            sine_data = await sine_viewer.view(sine_hub)
            bar_data = await bar_viewer.view(bar_hub)
            helix_data = await helix_viewer.view(helix_hub)

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
                            "z": helix_data["z"],
                            "marker": {"color": helix_data["marker.color"]},
                        }
                    ]
                }
            )

            await plt_hub.push(
                {
                    "Random Walk": rand_plt.to_dict(),
                    "Sine Wave": sine_plt.to_dict(),
                    "Bars": bar_plt.to_dict(),
                    "Helix": helix_plt.to_dict(),
                }
            )

            await asyncio.sleep(0.01)

    asyncio.run(main())
