import json

from eyegway.utils.plotting import Plot


class TestPlot:

    def test_plot_initialization(self):
        plot = Plot()
        assert plot.data == []
        assert plot.layout == {}
        assert plot.config == {}

    def test_plot_from_file(self, tmp_path):
        params = {
            "data": [{"x": [1, 2, 3], "y": [4, 5, 6]}],
            "layout": {"title": "Test Plot"},
            "config": {"responsive": True},
        }
        params_path = tmp_path / "params.json"
        with open(params_path, "w") as f:
            json.dump(params, f)

        plot = Plot.from_file(params_path=params_path)
        assert plot.data == params["data"]
        assert plot.layout == params["layout"]
        assert plot.config == params["config"]

    def test_plot_from_dict(self):
        params = {
            "data": [{"x": [1, 2, 3], "y": [4, 5, 6]}],
            "layout": {"title": "Test Plot"},
            "config": {"responsive": True},
        }
        plot = Plot.from_dict(params=params)
        assert plot.data == params["data"]
        assert plot.layout == params["layout"]
        assert plot.config == params["config"]

    def test_plot_pack(self):
        plot = Plot(data=[{"x": [1, 2, 3], "y": [4, 5, 6]}])
        packed_data = plot.to_dict()
        assert packed_data == {
            "data": [{"x": [1, 2, 3], "y": [4, 5, 6]}],
            "layout": {},
            "config": {},
        }

    def test_plot_update(self):
        plot = Plot(data=[{"x": [1, 2, 3], "y": [4, 5, 6]}])
        new_params = {
            "data": [{"x": [1, 2, 3], "y": [7, 8, 9]}],
            "layout": {"title": "Updated Plot"},
            "config": {"responsive": False},
        }
        plot.update(new_params)
        assert plot.data[0]["y"] == [7, 8, 9]
        assert plot.layout["title"] == "Updated Plot"
        assert plot.config["responsive"] is False
