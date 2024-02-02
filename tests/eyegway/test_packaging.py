import pytest
import eyegway.packaging as ep
from deepdiff import DeepDiff
import numpy as np


def simple_messages():
    return [
        "Hello, world!",
        1,
        4.312312321312312312,
        [1, 2, 3],
        [2.3, 2, [2, 3]],
    ]


def complex_messages():
    return [
        {"a": 1, "b": 2, "c": 3},
        {
            "image": np.random.randint(0, 255, (100, 100, 3)).astype(np.uint8),
            "tensor": np.random.rand(100, 100, 3),
            "tensor16": np.random.rand(100, 100, 3).astype(np.float16),
            "tensor32": np.random.rand(100, 100, 3).astype(np.float32),
            "tensor64": np.random.rand(19, 20, 33).astype(np.float64),
        },
        {
            "int": {
                "int16": np.random.randint(0, 255, (1, 1)).astype(np.int16),
                "int32": np.random.randint(0, 255, (10, 20, 30)).astype(np.int32),
                "int64": np.random.randint(0, 255, (1, 1, 1, 1)).astype(np.int64),
            },
            "uint": {
                "uint16": np.random.randint(0, 255, (40, 40)).astype(np.uint16),
                "uint32": np.random.randint(0, 255, (10, 20)).astype(np.uint32),
                "uint64": np.random.randint(0, 255, (30, 30)).astype(np.uint64),
            },
        },
        {
            "complex": np.random.uniform(-1, 1, (100, 100, 3)).astype(np.complex64),
        },
        {
            "buffer": np.random.uniform(-1, 1, (10,)).tobytes(),
            "another_buffer": b"hello world",
        },
    ]


def messages():
    return simple_messages() + complex_messages()


def generate(size, dtype):
    return np.random.uniform(size=size).astype(dtype)


class TestShapeMatching:
    @pytest.mark.parametrize(
        "shape, dtype, array, expected",
        [
            (..., ..., generate((10, 10, 3), np.float64), True),
            ((10, 10, 3), ..., generate((10, 10, 3), np.float64), True),
            ((10, 10, 3), ..., generate((10, 10, 3), np.float32), True),
            ((10, 10), ..., generate((10, 10, 3), np.float16), False),
            ((5, 5, 5), np.float32, generate((5, 5, 5), np.float16), False),
            ((5, ..., 5), np.float32, generate((5, 1, 5), np.float32), True),
            ((5, ..., 5), np.float32, generate((5, 2, 5), np.float32), True),
            ((..., ..., ...), np.float32, generate((1, 2, 3), np.float32), True),
            ((...,), np.float32, generate((1, 2, 3), np.float32), False),
            ((..., ..., 3), np.uint8, generate((256, 256, 3), np.uint8), True),
        ],
    )
    def test_match_shape(self, shape, dtype, array, expected):
        print(array.shape, array.dtype, shape, dtype)
        assert ep.match_shape(array, shape, dtype) == expected


class TestPackaging:
    @pytest.mark.parametrize("message", messages())
    def test_equality(self, message):
        # Multi Parser
        parser = ep.MultipleMessageParser()

        # Convert all images (..., ..., 3) / uint8 to PNG [so they are lossless]
        parser.add(
            ep.NumpyToImageMessageParser((..., ..., 3), np.uint8, ep.PNGImageEncoder())
        )

        # Convert all other numpy arrays to generic tensors
        parser.add(ep.NumpyToTensorMessageParser())

        # Multi unparsers
        unparser = ep.MultipleMessageUnparser(
            {
                ep.CustomMessageTypes.IMAGE.value: ep.NumpyFromImageMessageUnparser(),
                ep.CustomMessageTypes.TENSOR.value: ep.NumpyFromTensorMessageUnparser(),
            }
        )

        # Build custom pickpacker
        pickpacker = ep.MsgPacker(parser=parser, unparser=unparser)

        packed = pickpacker.pack(message)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)

        assert not DeepDiff(message, unpacked, ignore_numeric_type_changes=True)

    @pytest.mark.parametrize("message", messages())
    def test_smartpickpacker(self, message):
        # Smart pickpacker converts all images (..., ..., 3) / uint8 to JPEG [lossy]
        # all (..., ...) / uint8 images to PNG [lossless], and other numpy arrays to
        # generic tensors
        pickpacker = ep.DefaultMsgPacker()

        packed = pickpacker.pack(message)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)

        assert not DeepDiff(message, unpacked, exclude_types=[np.ndarray])

    def test_tiff(self):
        data = {
            "image": np.random.randint(0, 255, (100, 100, 3)).astype(np.uint8),
            "tensor": np.random.rand(100, 100, 3),
            "tensor16": np.random.rand(100, 100, 3).astype(np.float16),
            "tensor32": np.random.rand(100, 100, 3).astype(np.float32),
            "tensor64": np.random.rand(19, 20, 33).astype(np.float64),
        }

        # Multi Parser
        parser = ep.MultipleMessageParser()

        # Convert all numpy to TIFF images
        parser.add(ep.NumpyToImageMessageParser(..., ..., ep.TIFFImageEncoder()))

        # Multi unparsers
        unparser = ep.MultipleMessageUnparser()
        unparser.add(
            ep.CustomMessageTypes.IMAGE.value, ep.NumpyFromImageMessageUnparser()
        )

        # Build custom pickpacker
        pickpacker = ep.MsgPacker(parser=parser, unparser=unparser)

        packed = pickpacker.pack(data)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)

        assert not DeepDiff(data, unpacked)


class TestParserBuilding:

    def test_building(self):

        parser = ep.MultipleMessageParser(
            parsers=[
                ep.NumpyToImageMessageParser(
                    (..., ..., 3), np.uint8, ep.JPEGImageEncoder()
                ),
                ep.NumpyToImageMessageParser(
                    (..., ...), np.uint8, ep.PNGImageEncoder()
                ),
                ep.NumpyToImageMessageParser(..., np.float32, ep.TIFFImageEncoder()),
                ep.NumpyToImageMessageParser(..., ..., ep.TIFFImageEncoder()),
                ep.NumpyToImageMessageParser((10, 10, 3), ..., ep.TIFFImageEncoder()),
                ep.NumpyToTensorMessageParser(),
            ]
        )

        reparser = ep.MultipleMessageParser.build(str(parser))

        assert len(parser.subparsers) == len(reparser.subparsers)

        for idx, subparser in enumerate(parser.subparsers):
            assert str(subparser) == str(reparser.subparsers[idx])


# def test_buffer():
#     data = {"buffer": np.ones(1).tobytes()}
#     pickpacker = ap.PickPacker()

#     packed = pickpacker.pack(data)
#     print(data, packed)
