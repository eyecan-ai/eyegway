import typing as t

import loguru
import numpy as np
import pipelime.items as pli
import pipelime.sequences as pls

import eyegway.hubs.connectors as ehc


def model3d_converter(item: pli.Model3DItem) -> t.Any:
    if isinstance(item, pli.PLYModel3DItem):
        pcd = item()
        return {
            "eyegway_custom": "pointcloud",
            "vertices": pcd.vertices.astype(np.float32),
            "colors": (pcd.colors[:, :3] / 255.0).astype(np.float32),
        }
    else:
        raise Exception("Unknown item type")  # pragma: no cover


DEFAULT_ITEM_TO_PLAINDATA = {
    pli.NumpyItem: lambda item: item(),
    pli.MetadataItem: lambda item: item(),
    pli.BinaryItem: lambda item: item(),
    pli.Model3DItem: model3d_converter,
}

DEFAULT_PLAINDATA_TO_ITEM = {
    bytes: lambda data: pli.BinaryItem(data),
    dict: lambda data: pli.YamlMetadataItem(data),
    list: lambda data: pli.YamlMetadataItem(data),
    str: lambda data: pli.YamlMetadataItem(data),
    float: lambda data: pli.YamlMetadataItem(data),
    int: lambda data: pli.YamlMetadataItem(data),
    np.ndarray: lambda data: pli.NpyNumpyItem(data),
}

ItemToPlainDataCallable = t.Callable[[pli.Item], t.Any]
PlainDataToItemCallable = t.Callable[[t.Any], pli.Item]


class PipelimeHubConnector(ehc.HubConnector):
    def __init__(
        self,
        item_to_plaindata: list[tuple[type, ItemToPlainDataCallable]] = [],
        plaindata_to_item: list[tuple[type, PlainDataToItemCallable]] = [],
    ):
        self.custom_item_to_plaindata = item_to_plaindata
        self.custom_plaindata_to_item = plaindata_to_item

    def item_to_plaindata(self) -> dict[type, ItemToPlainDataCallable]:
        return {**DEFAULT_ITEM_TO_PLAINDATA, **dict(self.custom_item_to_plaindata)}

    def plaindata_to_item(self) -> dict[type, PlainDataToItemCallable]:
        return {**DEFAULT_PLAINDATA_TO_ITEM, **dict(self.custom_plaindata_to_item)}

    def world_to_hub(self, data: pls.Sample) -> dict:
        if not isinstance(data, pls.Sample):
            return data  # pragma: no cover

        output_data = {}
        for key in data:
            item = data[key]
            for item_type, converter in self.item_to_plaindata().items():
                if isinstance(item, item_type):
                    try:
                        output_data[key] = converter(item)
                        break
                    except Exception as e:  # pragma: no cover
                        loguru.logger.error(
                            f"Error converting {key} [{type(item)}] to plain data: {e}"
                        )
            else:  # pragma: no cover
                loguru.logger.warning(f"Item {key} [{type(item)}] is not allowed")
        return output_data

    def hub_to_world(self, data: dict) -> pls.Sample:
        if not isinstance(data, dict):
            return data  # pragma: no cover

        output_data = {}
        for key, value in data.items():
            for data_map_type, converter in self.plaindata_to_item().items():
                if isinstance(value, data_map_type):
                    try:
                        output_data[key] = converter(value)
                        break
                    except Exception as e:  # pragma: no cover
                        loguru.logger.error(
                            f"Error converting {key} [{type(value)}] to item: {e}"
                        )
            else:  # pragma: no cover
                loguru.logger.warning(f"Item {key} [{type(value)}] is not allowed")
        return pls.Sample(output_data)
