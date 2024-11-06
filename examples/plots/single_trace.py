from eyegway.hubs.sync import MessageHub
from eyegway.utils.plotting import Plot

years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009"]
money = ["39.7", "41.9", "44.6", "46.8", "49.8", "53.1", "56.9", "61.8", "65.7", "67.1"]
money_spent = {"type": "scatter", "x": years, "y": money}
plot_config = {"data": [money_spent]}
plot = Plot.from_dict("my_first_plot", plot_config)
hub = MessageHub.create("my_plot_hub")
hub.clear()
hub.push(plot.pack())
