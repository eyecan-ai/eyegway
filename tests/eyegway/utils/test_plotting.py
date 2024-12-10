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

    def test_plot_to_file(self, tmp_path):
        plot = Plot(
            data=[{"x": [1, 2], "y": [3, 4]}],
            layout={"title": "Test"},
            config={"responsive": True},
        )
        params_path = tmp_path / "plot_params.json"
        plot.to_file(params_path)
        with open(params_path) as f:
            saved_params = json.load(f)
        assert saved_params == plot.to_dict()

    def test_merge_nested_dicts(self):
        d1 = {"layout": {"title": "Old", "axis": {"x": {"range": [0, 10]}}}}
        d2 = {
            "layout": {
                "title": "New",
                "axis": {"x": {"range": [0, 20]}, "y": {"range": [0, 30]}},
            }
        }
        merged = Plot._merge(d1, d2)
        assert merged == {
            "layout": {
                "title": "New",
                "axis": {
                    "x": {"range": [0, 20]},
                    "y": {"range": [0, 30]},
                },
            }
        }

    def test_merge_extend_list(self):
        d1 = {"data": [{"x": [1]}]}
        d2 = {"data": [{"x": [2]}, {"x": [3]}]}
        merged = Plot._merge(d1, d2)
        assert merged == {"data": [{"x": [2]}, {"x": [3]}]}

    def test_update_with_more_data(self):
        plot = Plot(data=[{"x": [1], "y": [2]}])
        new_params = {
            "data": [
                {"x": [3, 5], "y": [4, 6]},
            ]
        }
        plot.update(new_params)
        assert plot.data == new_params["data"]
