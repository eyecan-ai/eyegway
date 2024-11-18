# FAKE STOCK DATA GENERATOR - DON'T USE ME IN REAL LIFE AND DON'T MIND ME
import threading  # noqa
from eyegway.utils.generators import DataPusher, RandomWalkGenerator
from eyegway.hubs.sync import MessageHub

stock_hub = MessageHub.create("stock_price_hub")
stock_hub.clear()
rand_pusher = DataPusher(RandomWalkGenerator("time", "price"), stock_hub, interval=0.5)
threading.Thread(target=rand_pusher.run_sync, daemon=True).start()
#######################################################################

# EXAMPLE CODE

import time  # noqa
from eyegway.hubs.viewers import ValueAccumulatorView  # noqa
from eyegway.utils.plotting import Plot  # noqa

stock_price = {"type": "scatter", "x": [], "y": []}
plot_config = {"data": [stock_price]}
plot = Plot.from_dict(plot_config)
hub = MessageHub.create("my_plot_hub")
hub.clear()
hub.push({"my_second_plot": plot.to_dict()})

source_hub = MessageHub.create("stock_price_hub")
print("Data generation and plot updating started...")  # noqa
while True:
    accumulator = ValueAccumulatorView(keys=["time", "price"])
    data = accumulator._sync_view(source_hub)
    plot.update({"data": [{"x": data["time"], "y": data["price"]}]})
    hub.push({"my_second_plot": plot.to_dict()})
    time.sleep(0.5)
