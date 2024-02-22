import typer as tp

cli_hubs = tp.Typer(
    name="hubs",
    no_args_is_help=True,
    add_completion=False,
)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Serve HUBS Rest API",
)
def rest_serve(
    host: str = tp.Option(
        "0.0.0.0",  # Default value
        "--host",
        "-h",
        help="Host to serve the API",
    ),
    port: int = tp.Option(
        55221,  # Default value
        "--port",
        "-p",
        help="Port to serve the API",
    ),
    redis_host: str = tp.Option(
        "localhost",  # Default value
        "--redis-host",
        "-rh",
        help="Redis host",
    ),
    redis_port: int = tp.Option(
        6379,  # Default value
        "--redis-port",
        "-rp",
        help="Redis port",
    ),
):
    import uvicorn

    import eyegway.hubs as eh
    import eyegway.hubs.rest.api as erha

    config = eh.HubsConfig(redis_host=redis_host, redis_port=redis_port)
    api = erha.HubsRestAPI(config=config)
    uvicorn.run(api, host=host, port=port)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Search HUBs",
)
def search():
    import eyegway.hubs.sync as ehs
    import rich

    hub = ehs.MessageHubManager.create()

    rich.print(hub.list())


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Info about an HUB",
)
def info(
    hub_name: str = tp.Option(
        ...,
        "--name",
        "-n",
        help="Hub name",
    )
):
    import eyegway.hubs.sync as ehs
    import rich

    hub = ehs.MessageHub.create(name=hub_name)

    rich.print(f"Hub |[red]{hub_name}[/red]| info:")
    rich.print("- Buffer size:", hub.buffer_size())
    rich.print("- History size:", hub.history_size())


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Clear HUB",
)
def clear(
    hub_name: str = tp.Option(
        ...,
        "--name",
        "-n",
        help="Hub name",
    )
):
    import eyegway.hubs.sync as ehs
    import rich

    hub = ehs.MessageHub.create(name=hub_name)
    hub.clear()
    rich.print(f"Hub |[red]{hub_name}[/red]| cleared!")


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Clear HUB History",
)
def clear_history(
    hub_name: str = tp.Option(
        ...,
        "--name",
        "-n",
        help="Hub name",
    )
):
    import eyegway.hubs.sync as ehs
    import rich

    hub = ehs.MessageHub.create(name=hub_name)
    hub.clear_history()
    rich.print(f"Hub |[red]{hub_name}[/red]| history cleared!")


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Clear HUB Buffer",
)
def clear_buffer(
    hub_name: str = tp.Option(
        ...,
        "--name",
        "-n",
        help="Hub name",
    )
):
    import eyegway.hubs.sync as ehs
    import rich

    hub = ehs.MessageHub.create(name=hub_name)
    hub.clear_buffer()
    rich.print(f"Hub |[red]{hub_name}[/red]| buffer cleared!")


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Pop HUB data to file",
)
def pop(
    hub_name: str = tp.Option(
        ...,
        "--name",
        "-n",
        help="Hub name",
    ),
    filename: str = tp.Option(
        ...,
        "--filename",
        "-f",
        help="File to save the data",
    ),
):
    import eyegway.hubs.sync as ehs
    import rich

    hub = ehs.MessageHub.create(name=hub_name)
    data = hub.pop(timeout=1)
    if data is None:
        rich.print(f"Hub |[red]{hub_name}[/red]| buffer is empty!")
        return

    with open(filename, "wb") as f:
        f.write(hub.packer.pack(data))

    rich.print(f"Hub |[red]{hub_name}[/red]| data popped to |[red]{filename}[/red]!")


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Print HUB history data",
)
def last(
    hub_name: str = tp.Option(
        ...,
        "--name",
        "-n",
        help="Hub name",
    ),
    offset: int = tp.Option(
        0,
        "--offset",
        "-o",
        help="History offset",
    ),
):
    import eyegway.hubs.sync as ehs
    import eyegway.packers as ep
    import rich

    hub = ehs.MessageHub.create(name=hub_name)
    data = hub.last(offset=offset)
    if data is None:
        rich.print(f"Hub |[red]{hub_name}[/red]| history[{offset}] is empty!")
        return
    ep.MessagePacker.pretty_print(data)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Info about packed data",
)
def pack_info(
    filename: str = tp.Option(
        ...,
        "--filename",
        "-f",
        help="Packed File",
    ),
):
    import eyegway.packers.factory as epf
    import eyegway.packers as ep

    data = open(filename, "rb").read()
    unpacked = epf.PackersFactory.default().unpack(data)
    ep.MessagePacker.pretty_print(unpacked)


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Stream a pipelime dataset to a HUB",
)
def stream_to(
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
    import loguru

    async def run():
        nonlocal keys

        # Create hub
        hub = eha.AsyncMessageHub.create(name=hub_name)

        # Add pipelime connector to parse input samples into plain dictionaries
        hub.connectors.append(ehcp.PipelimeHubConnector())

        # Clear buffer and history
        await hub.clear_history()

        # load dataset
        dataset = pls.SamplesSequence.from_underfolder(folder)

        # Filter keys if necessary
        keys = keys.split(",") if keys is not None else []
        if len(keys) > 0:
            dataset = dataset.map(pst.StageKeysFilter(key_list=keys))

        while True:
            for _, sample in enumerate(dataset):
                loguru.logger.info(f"Pushing sample: {list(sample.keys())}")
                await hub.push(sample)
                await asyncio.sleep(tick)

            if not loop:
                break

    asyncio.get_event_loop().run_until_complete(run())


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="View data streaming from HUB",
)
def stream_from(
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
        help="Keys to include in viewer",
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


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


@cli_hubs.command(
    short_help="Stream demo data to a HUB",
)
def stream_demo(
    hub_name: str = tp.Option(
        ...,
        "--hub-name",
        "-n",
        help="Hub name to stream to",
    ),
    tick: float = tp.Option(
        0.1,
        "--tick",
        "-t",
        help="Tick rate",
    ),
):
    import eyegway.hubs.asyn as eha
    import eyegway.utils as eut
    import asyncio
    import loguru

    async def run():
        # Create hub
        hub = eha.AsyncMessageHub.create(name=hub_name)

        generator = eut.DemoDataGenerator()

        while True:
            await hub.push(generator.generate())
            loguru.logger.info("Streaming ...")
            await asyncio.sleep(tick)

    asyncio.get_event_loop().run_until_complete(run())
