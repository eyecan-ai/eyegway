import pathlib as pl
import typing as t


class Plot:
    """
    Prepare and update plots with data from hubs.

    Attributes:
        data (Optional[List]): The data for the plot.
        layout (Optional[dict]): The layout configuration for the plot.
        config (Optional[dict]): The configuration for the plot.

    Example:
        # Basic example
        plot = Plot(name="example_plot")
        plot.update({"data": [{"x": [1, 2, 3], "y": [4, 5, 6]}]})

        # Example with layout and scatter data
        plot = Plot(
            data=[{"type": "scatter", "x": [1, 2, 3], "y": [4, 5, 6]}],
            layout={"title": "Scatter Plot Example"}
        )
        plot.update({"data": [{"x": [1, 2, 3], "y": [4, 5, 6]}]})
    """

    def __init__(
        self,
        data: t.Optional[t.List] = None,
        layout: t.Optional[dict] = None,
        config: t.Optional[dict] = None,
    ):
        if data is None:
            data = []

        if layout is None:
            layout = {}

        if config is None:
            config = {}

        self.data = data
        self.layout = layout
        self.config = config

    @classmethod
    def from_file(cls, params_path: pl.Path) -> "Plot":
        """
        Creates a Plot instance from a JSON file.

        Args:
            params_path (Path): The path to the JSON file containing plot parameters.

        Returns:
            Plot: A new Plot instance.
        """
        import json

        with open(params_path) as f:
            params = dict(json.load(f))
            return cls.from_dict(params=params)

    @classmethod
    def from_dict(cls, params: t.Dict) -> "Plot":
        """
        Creates a Plot instance from a dictionary.

        Args:
            params (Dict): A dictionary containing plot parameters.

        Returns:
            Plot: A new Plot instance.
        """
        return cls(**params)

    @staticmethod
    def _merge(d1: t.Dict[str, t.Any], d2: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        """
        Recursively merges two dictionaries.
        If there are nested dictionaries or lists, they are merged as well.

        Args:
            d1 (dict): The first dictionary.
            d2 (dict): The second dictionary.

        Returns:
            dict: The merged dictionary.
        """
        for key, value in d2.items():
            if key in d1:
                if isinstance(d1[key], dict) and isinstance(value, dict):
                    d1[key] = Plot._merge(d1[key], value)
                elif isinstance(d1[key], list) and isinstance(value, list):
                    for i in range(min(len(d1[key]), len(value))):
                        if isinstance(d1[key][i], dict) and isinstance(value[i], dict):
                            d1[key][i] = Plot._merge(d1[key][i], value[i])
                        else:
                            d1[key][i] = value[i]
                    if len(value) > len(d1[key]):
                        d1[key].extend(value[len(d1[key]) :])
                else:
                    d1[key] = value
            else:
                d1[key] = value
        return d1

    def to_dict(self) -> t.Dict[str, t.Any]:
        """
        Packs the plot data into a dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing the plot data ready to be pushed.
        """
        return {"data": self.data, "layout": self.layout, "config": self.config}

    def update(self, params: t.Dict) -> None:
        """
        Updates the plot with new parameters.

        Args:
            params (Dict): A dictionary containing new plot parameters.
        """
        self.data = [
            self._merge(o, n) for o, n in zip(self.data, params.get("data", []))
        ]
        self.layout = self._merge(self.layout, params.get("layout", self.layout))
        self.config = self._merge(self.config, params.get("config", self.config))
