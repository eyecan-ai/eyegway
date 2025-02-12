# Eyegway Plots Examples

This directory contains various examples demonstrating how to use the Eyegway library for data routing and visualization.

## Single Plot Example

This example demonstrates how to create a simple random walk plot using Eyegway.

**NOTE**: Ensure you have a running instance of Redis.

### Creating your first plot
Let's imagine we have a python task that generate some kind of logging data.
We want to visualize this data in real-time in a plot using `eyegway`.

For example we want to plot a scattered line representing money (in billions) spent on
pets in US over the years we can do the following:

```python
years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009"]
money = ["39.7", "41.9", "44.6", "46.8", "49.8", "53.1", "56.9", "61.8", "65.7", "67.1"]
```

To plot this in a scattered line plot we can create a config like this:

```python
money_spent = {
    "type": "scatter",
    "x": years,
    "y": money,
}
plot_config = {
    "data": [money_spent]
}
```
Now, the `plot_config` is a dictionary that contains the configuration for the plot, the information on how to write a plot configuration can be found in the [plotly.js documentation](https://plotly.com/javascript/).

Next step is to create a `Plot` object from a configuration:

```python
from eyegway.utils.plotting import Plot

plot = Plot.from_dict(plot_config)
```

Now we can push the plot to an `eyegway` hub:
    
```python
from eyegway.hubs.sync import MessageHub

hub = MessageHub.create("my_plot_hub")
hub.clear() # This to clear the hub from any previous plots attempts
hub.push({"my_first_plot": plot.to_dict()})
```

The full code is available in the [single_trace.py](examples/plots/single_trace.py) file, to run it:

```bash
python examples/plots/single_trace.py
```

Opening the `eyegway` UI should show the plot, you can access the UI by launching these two commands in separate terminals:

For REST Server:
```bash
eyegway hubs rest-serve
```
For UI:
```bash
cd web/eyegway-svelte
npm run dev
```

To show the plot, you need to: 
- select `my_plot_hub` from the top-right dropdown menu
- click on the `edit` button on the bottom right of the main application window
- click on the `add` button on the bottom right of the main application window
- select (or write) the name of the plot you want to show, in this case `my_first_plot`

If this is working correctly, you should see a plot showing the money spent on pets in the US over the years. But why stop here? Let's add another trace to the plot to make things more interesting.

### Adding another trace to the plot

Suppose that you want to show the `money spent on pets in US` and `people who died by falling down the stairs` in the same plot.

You can do this by adding another trace to the plot configuration:

```python
years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009"]
falls = ["1307", "1462", "1598", "1588", "1638", "1690", "1818", "1917", "1935", "1960"]
```

Notice that here we are adding an handle to the y-axis of the plot, this is done by adding the `yaxis` key to the trace configuration to specify the axis to which the trace belongs:
    
```python
stairs_falls = {
    "type": "scatter",
    "x": years,
    "y": falls,
    "yaxis": "y2",
}
```
Now, however, we need to represent both traces in the same plot, so we need to update the `plot_config` dictionary to include both traces and add also layout information to specify the range of the y-axes.
Notice that we are using the handle we previously defined in the trace configuration to specify the axis to which the trace belongs:

```python
plot_config = {
    "data": [money_spent, stairs_falls],
    "layout": {
        "yaxis": {
            "range": [30, 70],
            "title": "Money Spent on Pets",
            "tickprefix": "B$",
        },
        "yaxis2": {
            "range": [1300, 2000],
            "title": "People who died by falling down the stairs",
            "overlaying": "y",
            "side": "right",
        },
    },
}
```

Now, you can push the plot to the hub as before, the full code is available in the [multi_trace.py](examples/plots/multi_trace.py) file:

```bash
python examples/plots/multi_trace.py
```

If you follow the same steps as before to show the plot in the UI, you should see a plot showing the money spent on pets in the US and the number of people who died by falling down the stairs over the years.

They are creepingly similar, aren't they? 🤔

## Moving Data Example

Imagine you have a time series that moves over time, like a stock price, and you want to visualize it in real-time using `eyegway`.

The data is coming from a hub named `stock_price_hub`, where each item pop-ed from the hub is a dictionary with the keys `time` and `price`. 

```python
from eyegway.utils.plotting import Plot

stock_price = {"type": "scatter", "x": [], "y": []} # this time starting data is empty
plot_config = {"data": [stock_price]}
plot = Plot.from_dict(plot_config)
hub = MessageHub.create("my_plot_hub")
hub.clear()
hub.push({"my_second_plot": plot.to_dict()})
```

Our hub is updated with the new data in a separate process we are not aware of, we care
only about viewing the data aggregated in the way we want, for this we can use a viewer
object that will take care of the data aggregation.

```python
import time
from eyegway.hubs.viewers import ValueAccumulatorView
source_hub = MessageHub.create("stock_price_hub")
while True:
    accumulator = ValueAccumulatorView(keys=["time", "price"])
    data = accumulator._sync_view(source_hub)
    plot.update({"data": [{"x": data["time"], "y": data["price"]}]})
    hub.push({"my_second_plot": plot.to_dict()})
    time.sleep(0.5)
```
The full code is available in the [single_plot_moving.py](examples/plots/single_plot_moving.py) file.

```bash
python examples/plots/single_plot_moving.py
```

### Multiple plots

Now, the last step, how can I visualize multiple plots in the same window?

Let us imagine that we want to plot simultaneously `my_fist_plot` and `my_second_plot` in the same window.

We can simply merge them and push them in the same hub, e.g.:

```python
hub.push(
    {
        **{"my_first_plot": first_plot.to_dict()},
        **{"my_second_plot": second_plot.to_dict()},
    }
)
```

The full code is available in the [multi_plot_moving.py](examples/plots/multi_plot_moving.py) file.

```bash
python examples/plots/multi_plot_moving.py
```

If you need other examples check the ones starting with `advanced_`.