import numpy as np
import pytest
from deepdiff import DeepDiff

import eyegway.packers as ep
import eyegway.packers.images as epi
import eyegway.packers.numpy as ecp
import eyegway.packers.numpy as epn

from .commons import valid_numpy_messages


def generate(shape, dtype):
    return np.random.uniform(size=shape).astype(dtype)


def formats():
    return [
        (
            ".../...",
            epn.NumpyFormat(shape=..., dtype=...),
            True,
        ),
        (
            "(1,23,4)/uint8 ",
            epn.NumpyFormat(shape=(1, 23, 4), dtype=np.uint8),
            True,
        ),
        (
            "(1,23,4)/float32 ",
            epn.NumpyFormat(shape=(1, 23, 4), dtype=np.float32),
            True,
        ),
        (
            ".../ float64",
            epn.NumpyFormat(shape=..., dtype=np.float64),
            True,
        ),
        (
            "(10,10)/...",
            epn.NumpyFormat(shape=(10, 10), dtype=...),
            True,
        ),
        (
            "(10,10,3)/ float64 ",
            epn.NumpyFormat(shape=(10, 10, 3), dtype=np.float64),
            True,
        ),
        # falses
        (
            "(10,10,3)/float64",
            epn.NumpyFormat(shape=(10, 10, 3), dtype=np.float32),
            False,
        ),
        (
            "(100,10,3)/float32",
            epn.NumpyFormat(shape=(10, 10, 3), dtype=np.float32),
            False,
        ),
        (
            "(10,10,3   )/float32",
            epn.NumpyFormat(shape=(10, 10, 3), dtype=np.float64),
            False,
        ),
    ]


def pairs():
    return [
        (
            epn.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
            [
                (generate((256, 256, 3), np.uint8), True),
                (generate((256, 256), np.uint8), False),
                (generate((256, 256, 3), np.uint16), False),
                (generate((256, 256, 3), np.float32), False),
            ],
        ),
        (
            epn.NumpyFormat(shape=(..., ...), dtype=np.uint8),
            [
                (generate((256, 256, 3), np.uint8), False),
                (generate((256, 256), np.uint8), True),
            ],
        ),
        (
            epn.NumpyFormat(shape=..., dtype=...),
            [
                (generate((10, 10, 3), np.float64), True),
                (generate((10, 10, 3), np.float32), True),
                (generate((2,), np.float16), True),
            ],
        ),
        (
            epn.NumpyFormat(shape=(10, 10, 3), dtype=np.float64),
            [
                (generate((10, 10, 3), np.float64), True),
                (generate((10, 10, 3), np.float32), False),
                (generate((2,), np.float16), False),
            ],
        ),
        (
            epn.NumpyFormat(shape=(10, 10, 3), dtype=np.float32),
            [
                (generate((10, 10, 3), np.float64), False),
                (generate((10, 10, 3), np.float32), True),
                (generate((2,), np.float16), False),
            ],
        ),
        (
            epn.NumpyFormat(shape=(2,), dtype=np.float16),
            [
                (generate((10, 10, 3), np.float64), False),
                (generate((10, 10, 3), np.float32), False),
                (generate((2,), np.float16), True),
            ],
        ),
        (
            epn.NumpyFormat(shape=(10, 10), dtype=...),
            [
                (generate((10, 10, 3), np.float64), False),
                (generate((10, 10, 3), np.float32), False),
                (generate((2,), np.float16), False),
                (generate((10, 10), np.float16), True),
                (generate((10, 10), np.float32), True),
            ],
        ),
    ]


class TestNumpyFormat:

    @pytest.mark.parametrize("repr, format, expected", formats())
    def test_parsing(self, repr: str, format: epn.NumpyFormat, expected: bool):

        parsed_format = epn.NumpyFormat.parse(repr)
        if expected:
            assert parsed_format == format
            assert str(parsed_format) == str(format)

    @pytest.mark.parametrize("format, pairs", pairs())
    def test_matching(self, format: epn.NumpyFormat, pairs):
        for array, expected in pairs:
            assert format.match(array) == expected


def conversions():
    return [
        (
            "(...,...,3)/uint8 = image/jpeg",
            ecp.NumpyConversion(
                numpy_format=epn.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
                image_encoder=epi.JPEGImageEncoder(),
            ),
            True,
        ),
        (
            "(512,...)/uint16=image/png",
            ecp.NumpyConversion(
                numpy_format=epn.NumpyFormat(shape=(512, ...), dtype=np.uint16),
                image_encoder=epi.PNGImageEncoder(),
            ),
            True,
        ),
        (
            "(...)/...= image/tiff",
            ecp.NumpyConversion(
                numpy_format=epn.NumpyFormat(shape=..., dtype=...),
                image_encoder=epi.TIFFImageEncoder(),
            ),
            True,
        ),
    ]


class TestConversion:

    @pytest.mark.parametrize("repr, conversion, expected", conversions())
    def test_parsing(self, repr: str, conversion: ecp.NumpyConversion, expected: bool):

        parsed = ecp.NumpyConversion.parse(repr)
        if expected:
            assert parsed == conversion
            assert str(parsed) == str(conversion)
            assert ecp.NumpyConversion.parse(str(conversion)) == conversion
            assert ecp.NumpyConversion.parse(str(parsed)) == parsed

    def test_encoding(self):
        conversion = ecp.NumpyConversion(
            numpy_format=epn.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
            image_encoder=epi.TIFFImageEncoder(),
        )

        array = generate((256, 256, 3), np.uint8)

        assert conversion.match(array)

        encoded = conversion.encode(array)
        assert isinstance(encoded, bytes)

        decoded = conversion.decode(encoded)
        assert np.all(array == decoded)


class TestNumpyPackers:

    @pytest.mark.parametrize("message", valid_numpy_messages())
    def test_equality(self, message):
        # Multi Parser

        conversions = [
            epn.NumpyConversion(
                numpy_format=epn.NumpyFormat(
                    shape=(..., ..., 3),
                    dtype=np.uint8,
                ),
                image_encoder=epi.PNGImageEncoder(),
            ),
        ]

        parser = ep.MessageParserCompose(
            parsers=[epn.NumpyMessageParser(numpy_conversions=conversions)]
        )

        unparser = ep.MessageUnparserCompose(unparsers=[epn.NumpyMessageUnparser()])

        # Build custom pickpacker
        pickpacker = ep.MessagePacker(parser=parser, unparser=unparser)

        packed = pickpacker.pack(message)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)

        assert not DeepDiff(message, unpacked, ignore_numeric_type_changes=True)

    def test_tiff(self):
        data = {
            "image": np.random.randint(0, 255, (100, 100, 3)).astype(np.uint8),
            "tensor": np.random.rand(100, 100, 3),
            "tensor16": np.random.rand(100, 100, 3).astype(np.float16),
            "tensor32": np.random.rand(100, 100, 3).astype(np.float32),
            "tensor64": np.random.rand(19, 20, 33).astype(np.float64),
        }

        conversions = [
            epn.NumpyConversion(
                numpy_format=epn.NumpyFormat(
                    shape=...,
                    dtype=...,
                ),
                image_encoder=epi.TIFFImageEncoder(),
            ),
        ]

        parser = ep.MessageParserCompose(
            parsers=[epn.NumpyMessageParser(numpy_conversions=conversions)]
        )

        unparser = ep.MessageUnparserCompose(unparsers=[epn.NumpyMessageUnparser()])

        # Build custom pickpacker
        pickpacker = ep.MessagePacker(parser=parser, unparser=unparser)

        packed = pickpacker.pack(data)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)

        ep.MessagePacker.pretty_print(unpacked)

        assert not DeepDiff(data, unpacked)
