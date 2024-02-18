import eyegway.hubs.connectors as ehc
import pipelime.sequences as pls
import pipelime.items as pli
import loguru
import numpy as np
import typing as t

DEFAULT_ITEM_TO_PLAINDATA = {
    pli.NumpyItem: lambda item: item(),
    pli.MetadataItem: lambda item: item(),
    pli.BinaryItem: lambda item: item(),
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
        item_to_plaindata: t.List[t.Tuple[type, ItemToPlainDataCallable]] = [],
        plaindata_to_item: t.List[t.Tuple[type, PlainDataToItemCallable]] = [],
    ):
        self.custom_item_to_plaindata = item_to_plaindata
        self.custom_plaindata_to_item = plaindata_to_item

    def item_to_plaindata(self) -> t.Dict[type, ItemToPlainDataCallable]:
        return {**DEFAULT_ITEM_TO_PLAINDATA, **dict(self.custom_item_to_plaindata)}

    def plaindata_to_item(self) -> t.Dict[type, PlainDataToItemCallable]:
        return {**DEFAULT_PLAINDATA_TO_ITEM, **dict(self.custom_plaindata_to_item)}

    def world_to_hub(self, data: pls.Sample) -> dict:
        if not isinstance(data, pls.Sample):
            return data  # pragma: no cover

        output_data = {}
        for key in data:
            item = data[key]
            found = False
            for item_type, converter in self.item_to_plaindata().items():
                if isinstance(item, item_type):
                    try:
                        output_data[key] = converter(item)
                        found = True
                        break
                    except Exception as e:  # pragma: no cover
                        loguru.logger.error(
                            f"Error converting {key} [{type(item)}] to plain data: {e}"
                        )
            if not found:
                loguru.logger.warning(f"Item {key} [{type(item)}] is not allowed")
        return output_data

    def hub_to_world(self, data: dict) -> pls.Sample:
        if not isinstance(data, dict):
            return data  # pragma: no cover

        output_data = {}
        for key, value in data.items():
            found = False

            for data_map_type, converter in self.plaindata_to_item().items():
                if isinstance(value, data_map_type):
                    try:
                        output_data[key] = converter(value)
                        found = True
                        break
                    except Exception as e:  # pragma: no cover
                        loguru.logger.error(
                            f"Error converting {key} [{type(value)}] to item: {e}"
                        )
            if not found:  # pragma: no cover
                loguru.logger.warning(f"Item {key} [{type(value)}] is not allowed")
        return pls.Sample(output_data)
