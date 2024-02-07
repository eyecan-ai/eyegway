import pipelime.sequences as pls
import pipelime.stages as pst
import eyegway.hubs.asyn as eha
import eyegway.hubs.connectors.pipelime as ehcp
import asyncio
import typer as tp
import pipelime.sequences as pls
import typing as t
import pipelime.items as pli
import numpy as np


def pointcloud_to_data(item: pli.Model3DItem) -> t.Any:
    if isinstance(item, pli.PLYModel3DItem):
        pcd = item()
        return {
            "vertices": pcd.vertices.astype(np.float32),
            "colors": (pcd.colors[:, :3] / 255.0).astype(np.float32),
        }
    else:
        raise Exception("Unknown item type")


async def run(
    folder: str,
    hub_name: str,
    keys: t.Optional[str] = None,
    tick: float = 0.1,
    loop: bool = False,
):

    dataset = pls.SamplesSequence.from_underfolder(folder)

    # Create hub
    hub = eha.AsyncMessageHub.create(name=hub_name)

    await hub.clear_history()
    await hub.clear_buffer()

    # Add pipelime connector to parse input samples into plain dictionaries
    hub.connectors.append(
        ehcp.PipelimeHubConnector(
            item_to_plaindata=[(pli.Model3DItem, pointcloud_to_data)]
        )
    )

    await hub.clear_history()
    await hub.clear_buffer()

    # load dataset
    dataset = pls.SamplesSequence.from_underfolder(folder)

    # Filter keys if necessary
    keys = keys.split(",") if keys is not None else []
    if len(keys) > 0:
        dataset = dataset.map(pst.StageKeysFilter(key_list=keys))

    while True:
        for _, sample in enumerate(dataset):
            await hub.push(sample)

        if not loop:
            break


def pipelime_sender(
    folder: str = tp.Option(..., "--folder", "-f", help="Folder with the dataset"),
    hub_name: str = tp.Option(..., "--hub-name", "-n", help="Name of the hub"),
):
    asyncio.get_event_loop().run_until_complete(run(folder=folder, hub_name=hub_name))


if __name__ == '__main__':
    tp.run(pipelime_sender)
