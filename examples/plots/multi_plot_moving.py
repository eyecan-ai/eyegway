# FAKE STOCK DATA GENERATOR - DON'T USE ME IN REAL LIFE AND DON'T MIND ME
import threading  # noqa
from eyegway.utils.generators import DataPusher, RandomWalkGenerator
from eyegway.hubs.sync import MessageHub

stock_hub = MessageHub.create("stock_price_hub")
stock_hub.clear()
rand_pusher = DataPusher(RandomWalkGenerator("time", "price"), stock_hub, interval=0.5)
threading.Thread(target=rand_pusher.run_sync, daemon=True).start()
#######################################################################

# from multi_trace.py
from eyegway.utils.plotting import Plot  # noqa

years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009"]
money = ["39.7", "41.9", "44.6", "46.8", "49.8", "53.1", "56.9", "61.8", "65.7", "67.1"]
falls = ["1307", "1462", "1598", "1588", "1638", "1690", "1818", "1917", "1935", "1960"]
money_spent = {"type": "scatter", "x": years, "y": money}
stairs_falls = {"type": "scatter", "x": years, "y": falls, "yaxis": "y2"}
first_plot_config = {
    "data": [money_spent, stairs_falls],
    "layout": {
        "yaxis": {
            "range": [30, 70],
            "title": "Money Spent on Pets",
            "tickprefix": "B$",
        },
        "yaxis2": {
            "range": [1200, 2000],
            "title": "People who died by falling down the stairs",
            "overlaying": "y",
            "side": "right",
        },
    },
}
first_plot = Plot.from_dict("my_first_plot", first_plot_config)

# from single_trace_moving.py

import time  # noqa
from eyegway.hubs.viewers import ValueAccumulatorView  # noqa

stock_price = {"type": "scatter", "x": [], "y": []}
second_plot_config = {"data": [stock_price]}
second_plot = Plot.from_dict("my_second_plot", second_plot_config)

# COMMON PART

hub = MessageHub.create("my_plot_hub")
hub.clear()

source_hub = MessageHub.create("stock_price_hub")
print("Data generation and plot updating started...")  # noqa
while True:
    accumulator = ValueAccumulatorView(keys=["time", "price"])
    data = accumulator.view(source_hub)
    second_plot.update({"data": [{"x": data["time"], "y": data["price"]}]})
    hub.push({**first_plot.pack(), **second_plot.pack()})
    time.sleep(0.5)
