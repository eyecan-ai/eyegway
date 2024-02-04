import pipelime.sequences as pls
import pipelime.stages as pst
import pipelime.items as pli
import eyegway.hubs as eh
import eyegway.utils as eut
import eyegway.packers as ep
import eyegway.packers.numpy as epn
import eyegway.packers.images as epi
import eyegway.packers.pipelime as epp
import asyncio
import time
import loguru
import albumentations as A
import numpy as np


async def run():
    hub_name = "test"
    image_resize = 512
    folder = '/Users/daniele/Downloads/dataset'
    tick = 1.0
    keys = None

    # load dataset
    dataset = pls.SamplesSequence.from_underfolder(folder)

    # Conversions
    conversions = [
        #
        # Convert (..., ..., 3)/uint8 to JPEG
        #
        epn.NumpyConversion(
            numpy_format=epn.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
            image_encoder=epi.JPEGImageEncoder(),
        ),
        #
        # Convert (..., ...)/uint8 to PNG
        #
        epn.NumpyConversion(
            numpy_format=epn.NumpyFormat(shape=(..., ...), dtype=np.uint8),
            image_encoder=epi.PNGImageEncoder(),
        ),
    ]

    # Parser
    parser = ep.MessageParserCompose(
        parsers=[
            epn.NumpyMessageParser(numpy_conversions=conversions),
            epp.SampleMessageParser(),
            epp.ItemMessageParser(),
        ]
    )

    # Unparser
    unparser = ep.MessageUnparserCompose(unparsers=[epn.NumpyMessageUnparser()])

    # Build Packer
    packer = ep.MessagePacker(parser=parser, unparser=unparser)

    data = {
        "name": "test",
        "data": np.random.rand(512, 512, 3),
    }

    packed = packer.pack(dataset[0])
    # unpacked = packer.unpack(packed)

    # print(unpacked)

    # # Create hub
    # hub = eh.AsyncMessageHub.create(name=hub_name)

    # await hub.clear_history()

    # # Create image resize transform
    # transform = A.Compose([A.SmallestMaxSize(max_size=image_resize)])

    # # Filter keys if necessary
    # keys = keys.split(",") if keys is not None else []
    # if len(keys) > 0:
    #     dataset = dataset.map(pst.StageKeysFilter(key_list=keys))

    # packer = ep.MessagePacker(
    #     parser=ep.MessageParserCompose(
    #         parsers=[
    #             epp.ItemMessageParser(),
    #             epn.NumpyMessageParser(),
    #             epp.SampleMessageParser(),
    #         ]
    #     ),
    #     unparser=ep.MessageUnparserCompose(unparsers=[epn.NumpyMessageUnparser()]),
    # )

    # for sample_idx, sample in enumerate(dataset):

    #     packed = packer.pack(sample)
    #     await asyncio.sleep(tick)


if __name__ == "__main__":
    asyncio.run(run())
