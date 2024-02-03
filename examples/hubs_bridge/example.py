import numpy as np
import asyncio
import typing as t
import eyegway.hubs as eh
import eyegway.utils as eut
import pipelime.stages as pst
import pipelime.sequences as pls
import pipelime.items as pli


class Connector(eh.MessageHubConnector):

    def data_out(self, data: t.Any) -> pls.Sample:
        sample_data = {}
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], np.ndarray):
                    sample_data[key] = pli.NpyNumpyItem(data[key])
                elif isinstance(data[key], dict):
                    sample_data[key] = pli.YamlMetadataItem(data[key])

        return pls.Sample(sample_data)

    def data_in(self, data: pls.Sample) -> t.Any:
        output_data = {}
        for key in data:
            output_data[key] = data[key]()
        return output_data


def stage(data: t.Any) -> t.Any:

    for key in data.keys():
        print(key, type(data[key]))

    import albumentations as A

    stage = pst.StageAlbumentations(
        transform=A.Compose(
            [
                A.SmallestMaxSize(50),
                A.ShiftScaleRotate(rotate_limit=20, p=0.5),
                A.HueSaturationValue(p=0.5),
            ]
        ),
        keys_to_targets={"left_image": "image"},
        output_key_format="*",
    )

    data = stage(data)
    return data


if __name__ == '__main__':

    async def run():
        start_hub_name = "test"
        end_hub_name = "modified"

        start_hub = eh.AsyncMessageHub.create(start_hub_name)
        end_hub = eh.AsyncMessageHub.create(end_hub_name)

        start_hub.connector = Connector()
        end_hub.connector = Connector()

        while True:
            with eut.LoguruTimer("Pop"):
                data = await start_hub.pop(timeout=0)
            with eut.LoguruTimer("Stage"):
                data = stage(data)
            await end_hub.push(data)

    asyncio.run(run())
