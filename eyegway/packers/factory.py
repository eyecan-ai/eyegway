import eyegway.packers as ep
import eyegway.packers.numpy as epn
import eyegway.packers.images as epi
import numpy as np


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
    parser = ep.MessageParserCompose(
        parsers=[epn.NumpyMessageParser(numpy_conversions=conversions)]
    )

    # Unparser
    unparser = ep.MessageUnparserCompose(unparsers=[epn.NumpyMessageUnparser()])

    # Build Packer
    return ep.MessagePacker(parser=parser, unparser=unparser)


def message_packer_raw() -> ep.MessagePacker:

    # Parser, all numpy to simple tensors
    parser = ep.MessageParserCompose(parsers=[epn.NumpyMessageParser()])

    # Unparser
    unparser = ep.MessageUnparserCompose(unparsers=[epn.NumpyMessageUnparser()])

    # Build Packer
    return ep.MessagePacker(parser=parser, unparser=unparser)


class PackersFactory:
    PACKERS = {
        "default": message_packer_smart_images,
        "smart_images": message_packer_smart_images,
        "raw": message_packer_raw,
    }

    @classmethod
    def create(cls, name: str) -> ep.MessagePacker:
        if name not in cls.PACKERS:
            raise ValueError(f"Unknown packer: {name}")
        return cls.PACKERS[name]()

    @classmethod
    def default(cls) -> ep.MessagePacker:
        return cls.create("default")
