import typing as t

import numpy as np

import eyegway.packers as ep
import eyegway.packers.images as epi
import eyegway.packers.numpy as epn


def message_packer_smart_images() -> ep.MessagePacker:

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
    parser = epn.NumpyMessageParser(numpy_conversions=conversions)

    # Unparser
    unparser = epn.NumpyMessageUnparser()

    # Build Packer
    return ep.MessagePacker(parser=parser, unparser=unparser)


def message_packer_raw() -> ep.MessagePacker:

    # Parser, all numpy to simple tensors
    parser = epn.NumpyMessageParser()

    # Unparser
    unparser = epn.NumpyMessageUnparser()

    # Build Packer
    return ep.MessagePacker(parser=parser, unparser=unparser)


class PackersFactory:
    PACKERS: t.ClassVar = {
        "default": message_packer_smart_images,
        "smart_images": message_packer_smart_images,
        "raw": message_packer_raw,
    }

    @classmethod
    def create(cls, name: str | None = None) -> ep.MessagePacker:
        if name is None:
            name = "default"
        if name not in cls.PACKERS:
            raise ValueError(f"Unknown packer: {name}")  # pragma: no cover
        return cls.PACKERS[name]()

    @classmethod
    def default(cls) -> ep.MessagePacker:
        return cls.create("default")
