import eyegway.hubs.connectors as ehc
import pipelime.sequences as pls
import pipelime.items as pli
import loguru
import numpy as np


ITEM_TO_PLAINDATA = {
    pli.NumpyItem: lambda item: item(),
    pli.MetadataItem: lambda item: item(),
    pli.BinaryItem: lambda item: item(),
}

PLAINDATA_TO_ITEM = {
    bytes: lambda data: pli.BinaryItem(data),
    dict: lambda data: pli.YamlMetadataItem(data),
    list: lambda data: pli.YamlMetadataItem(data),
    str: lambda data: pli.YamlMetadataItem(data),
    float: lambda data: pli.YamlMetadataItem(data),
    int: lambda data: pli.YamlMetadataItem(data),
    np.ndarray: lambda data: pli.NpyNumpyItem(data),
}


class PipelimeHubConnector(ehc.HubConnector):

    def world_to_hub(self, data: pls.Sample) -> dict:
        if not isinstance(data, pls.Sample):
            return data  # pragma: no cover

        output_data = {}
        for key in data:
            item = data[key]
            found = False
            for item_type, converter in ITEM_TO_PLAINDATA.items():
                if isinstance(item, item_type):
                    output_data[key] = converter(item)
                    found = True
                    break
            if not found:
                loguru.logger.warning(f"Item {key} [{type(item)}] is not allowed")
        return output_data

    def hub_to_world(self, data: dict) -> pls.Sample:
        if not isinstance(data, dict):
            return data  # pragma: no cover

        output_data = {}
        for key, value in data.items():
            found = False

            for data_map_type, converter in PLAINDATA_TO_ITEM.items():
                if isinstance(value, data_map_type):
                    output_data[key] = converter(value)
                    found = True
                    break
            if not found:
                loguru.logger.warning(f"Item {key} [{type(value)}] is not allowed")
        return pls.Sample(output_data)
