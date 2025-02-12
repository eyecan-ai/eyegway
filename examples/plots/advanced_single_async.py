from pathlib import Path

from rich import print

import eyegway.utils.generators as eug
from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.viewers import ValueAccumulatorView
from eyegway.utils.plotting import Plot

if __name__ == "__main__":

    import asyncio

    async def main():
        # Here we create the hub from which the data will be popped and
        # the one to which the data will be pushed
        rand_hub = AsyncMessageHub.create("random_walk")
        await rand_hub.clear()

        plt_hub = AsyncMessageHub.create("plot_hub")
        await plt_hub.clear()

        # Here we choose the way in which data is aggregated and displayed in plot
        # the ValueAccumulatorView is used to accumulate the data for every key
        rand_viewer = ValueAccumulatorView(keys=["x", "y"])

        # Here we create the data pusher that will push the generated data to the hub
        rand_pusher = eug.DataPusher(eug.RandomWalkGenerator(), rand_hub, interval=0.01)

        # Here we create the plot that will be updated with the data from the hub
        rand_plt = Plot.from_file(Path("basic_plots/chart_red.json"))

        rand_task = asyncio.create_task(rand_pusher.run_async())
        rand_task.add_done_callback(lambda _: print("Data generation stopped"))

        # We start the threads for the data generation and plot updating
        print(
            "Data generation and plot updating started...\n"
            "Plot names: [yellow]Random Walk[/yellow], "
            "[red]Press Ctrl+C to stop the data generation and plot updating[/red]"
        )

        while True:
            data = await rand_viewer.view(rand_hub)
            rand_plt.update({"data": [{"x": data["x"], "y": data["y"]}]})
            await plt_hub.push({"Random Walk": rand_plt.to_dict()})
            await asyncio.sleep(0.01)

    asyncio.run(main())
