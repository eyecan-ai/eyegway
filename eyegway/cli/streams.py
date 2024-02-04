import typer as tp

cli_streams = tp.Typer(
    name="streams",
    no_args_is_help=True,
    add_completion=False,
    help="Stream data to and from a hub",
)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_streams.command(
    short_help="Stream a pipelime dataset to a hub",
)
def pipelime(
    folder: str = tp.Option(
        ...,
        "--input-folder",
        "-i",
        help="Packed file to load",
    ),
    hub_name: str = tp.Option(
        ...,
        "--hub-name",
        "-n",
        help="Hub name to stream to",
    ),
    tick: float = tp.Option(
        0.01,
        "--tick",
        "-t",
        help="Tick rate",
    ),
    loop: bool = tp.Option(
        False,
        "--loop",
        "-l",
        help="Infinitely loop the sequence",
    ),
    keys: str = tp.Option(
        None,
        "--keys",
        "-k",
        help="Keys to include in the sequence",
    ),
):
    import pipelime.sequences as pls
    import pipelime.stages as pst
    import eyegway.hubs.asyn as eha
    import eyegway.hubs.connectors.pipelime as ehcp
    import asyncio

    async def run():
        nonlocal keys

        # Create hub
        hub = eha.AsyncMessageHub.create(name=hub_name)

        # Add pipelime connector to parse input samples into plain dictionaries
        hub.connectors.append(ehcp.PipelimeHubConnector())

        await hub.clear_history()

        # load dataset
        dataset = pls.SamplesSequence.from_underfolder(folder)

        # Filter keys if necessary
        keys = keys.split(",") if keys is not None else []
        if len(keys) > 0:
            dataset = dataset.map(pst.StageKeysFilter(key_list=keys))

        while True:
            for _, sample in enumerate(dataset):
                await hub.push(sample)
                await asyncio.sleep(tick)

            if not loop:
                break

    asyncio.run(run())


@cli_streams.command(
    short_help="Stream a pipelime dataset to a hub",
)
def viewer(
    hub_name: str = tp.Option(
        ...,
        "--hub-name",
        "-n",
        help="Hub name to stream to",
    ),
    keys: str = tp.Option(
        None,
        "--keys",
        "-k",
        help="Image Keys to include in viewer",
    ),
    image_resize: int = tp.Option(
        380,
        "--image-resize",
        "-r",
        help="Image resize",
    ),
):
    import eyegway.hubs.asyn as eha
    import eyegway.packers.numpy as epn
    import eyegway.hubs.connectors.pipelime as ehcp
    import asyncio
    import loguru
    import albumentations as A
    import numpy as np
    import cv2
    import rich
    import typing as t

    async def run():
        nonlocal keys

        # What is an image?
        images_format = [
            epn.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
            epn.NumpyFormat(shape=(..., ...), dtype=np.uint8),
            epn.NumpyFormat(shape=(..., ...), dtype=...),
        ]

        # Helper to check if value is an image
        def is_image(value: t.Any):
            return (
                any([m.match(value) for m in images_format])
                if isinstance(value, np.ndarray)
                else False
            )

        # Create hub
        hub = eha.AsyncMessageHub.create(name=hub_name)

        # Add pipelime connector to parse input samples into plain dictionaries
        hub.connectors.append(ehcp.PipelimeHubConnector())

        # Create transforms to resize and center images in a square
        transform = A.Compose(
            [
                A.LongestMaxSize(max_size=image_resize),
                A.PadIfNeeded(
                    min_height=image_resize,
                    min_width=image_resize,
                    border_mode=cv2.BORDER_CONSTANT,
                    value=[0, 0, 0],
                ),
            ]
        )

        # Helper to display images, creates a colored version of any image and adds
        # borders
        def displayable_image(image: np.ndarray):
            image = transform(image=image)['image']
            image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            if len(image.shape) == 2:
                image = cv2.applyColorMap(image, cv2.COLORMAP_MAGMA)
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.copyMakeBorder(image, 0, 0, 0, 3, cv2.BORDER_CONSTANT)
            return image

        # Filter keys if necessary, if no keys are provided the viewer dies
        keys = keys.split(",") if keys is not None else []
        if len(keys) == 0:
            loguru.logger.error("No keys to visualize")
            raise tp.Abort()

        while True:
            # Get last data in history
            data = await hub.pop()

            # No data? wait a bit
            if data is None:
                await asyncio.sleep(0.1)
                loguru.logger.warning("No data found")
                continue

            # Check if data is a dictionary, if not, skip
            # if not isinstance(data, dict):
            #     loguru.logger.error("Viewer can manipulate only dictionary Data")
            #     continue

            images = []
            metadata = []
            for key in keys:
                if key in data:
                    value = data[key]()
                    if is_image(value):
                        images.append(displayable_image(value))
                    else:
                        metadata.append((key, value))

            # No images or metadata? wait a bit
            if len(images) == 0 and len(metadata) == 0:
                loguru.logger.warning("No data found with provided keys")
                continue

            # horizontal stack images with white space
            if len(images) > 0:
                images = cv2.hconcat(images)
                cv2.imshow("Viewer", images)
                cv2.waitKey(1)

            if len(metadata) > 0:
                for key, value in metadata:
                    rich.print(f"{key}\n {value}")

    asyncio.run(run())
