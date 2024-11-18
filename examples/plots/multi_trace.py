from eyegway.hubs.sync import MessageHub
from eyegway.utils.plotting import Plot

years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009"]
money = ["39.7", "41.9", "44.6", "46.8", "49.8", "53.1", "56.9", "61.8", "65.7", "67.1"]
falls = ["1307", "1462", "1598", "1588", "1638", "1690", "1818", "1917", "1935", "1960"]
money_spent = {"type": "scatter", "x": years, "y": money}
stairs_falls = {"type": "scatter", "x": years, "y": falls, "yaxis": "y2"}
plot_config = {
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
plot = Plot.from_dict(plot_config)
hub = MessageHub.create("my_plot_hub")
hub.clear()
hub.push({"my_first_plot": plot.to_dict()})
