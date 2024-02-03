import eyegway.packaging as ecp
import numpy as np
import pytest


def generate(shape, dtype):
    return np.random.uniform(size=shape).astype(dtype)


def formats():
    return [
        (
            ".../...",
            ecp.NumpyFormat(shape=..., dtype=...),
            True,
        ),
        (
            "(1,23,4)/uint8 ",
            ecp.NumpyFormat(shape=(1, 23, 4), dtype=np.uint8),
            True,
        ),
        (
            "(1,23,4)/float32 ",
            ecp.NumpyFormat(shape=(1, 23, 4), dtype=np.float32),
            True,
        ),
        (
            ".../ float64",
            ecp.NumpyFormat(shape=..., dtype=np.float64),
            True,
        ),
        (
            "(10,10)/...",
            ecp.NumpyFormat(shape=(10, 10), dtype=...),
            True,
        ),
        (
            "(10,10,3)/ float64 ",
            ecp.NumpyFormat(shape=(10, 10, 3), dtype=np.float64),
            True,
        ),
        # falses
        (
            "(10,10,3)/float64",
            ecp.NumpyFormat(shape=(10, 10, 3), dtype=np.float32),
            False,
        ),
        (
            "(100,10,3)/float32",
            ecp.NumpyFormat(shape=(10, 10, 3), dtype=np.float32),
            False,
        ),
        (
            "(10,10,3   )/float32",
            ecp.NumpyFormat(shape=(10, 10, 3), dtype=np.float64),
            False,
        ),
    ]


def pairs():
    return [
        (
            ecp.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
            [
                (generate((256, 256, 3), np.uint8), True),
                (generate((256, 256), np.uint8), False),
                (generate((256, 256, 3), np.uint16), False),
                (generate((256, 256, 3), np.float32), False),
            ],
        ),
        (
            ecp.NumpyFormat(shape=(..., ...), dtype=np.uint8),
            [
                (generate((256, 256, 3), np.uint8), False),
                (generate((256, 256), np.uint8), True),
            ],
        ),
        (
            ecp.NumpyFormat(shape=..., dtype=...),
            [
                (generate((10, 10, 3), np.float64), True),
                (generate((10, 10, 3), np.float32), True),
                (generate((2,), np.float16), True),
            ],
        ),
        (
            ecp.NumpyFormat(shape=(10, 10, 3), dtype=np.float64),
            [
                (generate((10, 10, 3), np.float64), True),
                (generate((10, 10, 3), np.float32), False),
                (generate((2,), np.float16), False),
            ],
        ),
        (
            ecp.NumpyFormat(shape=(10, 10, 3), dtype=np.float32),
            [
                (generate((10, 10, 3), np.float64), False),
                (generate((10, 10, 3), np.float32), True),
                (generate((2,), np.float16), False),
            ],
        ),
        (
            ecp.NumpyFormat(shape=(2,), dtype=np.float16),
            [
                (generate((10, 10, 3), np.float64), False),
                (generate((10, 10, 3), np.float32), False),
                (generate((2,), np.float16), True),
            ],
        ),
        (
            ecp.NumpyFormat(shape=(10, 10), dtype=...),
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
    def test_parsing(self, repr: str, format: ecp.NumpyFormat, expected: bool):

        parsed_format = ecp.NumpyFormat.parse(repr)
        if expected:
            assert parsed_format == format
            assert str(parsed_format) == str(format)

    @pytest.mark.parametrize("format, pairs", pairs())
    def test_matching(self, format: ecp.NumpyFormat, pairs):
        for array, expected in pairs:
            assert format.match(array) == expected


def conversions():
    return [
        (
            "(...,...,3)/uint8 = image/jpeg",
            ecp.NumpyConversion(
                numpy_format=ecp.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
                image_encoder=ecp.JPEGImageEncoder(),
            ),
            True,
        ),
        (
            "(512,...)/uint16=image/png",
            ecp.NumpyConversion(
                numpy_format=ecp.NumpyFormat(shape=(512, ...), dtype=np.uint16),
                image_encoder=ecp.PNGImageEncoder(),
            ),
            True,
        ),
        (
            "(...)/...= image/tiff",
            ecp.NumpyConversion(
                numpy_format=ecp.NumpyFormat(shape=..., dtype=...),
                image_encoder=ecp.TIFFImageEncoder(),
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
            numpy_format=ecp.NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
            image_encoder=ecp.TIFFImageEncoder(),
        )

        array = generate((256, 256, 3), np.uint8)

        assert conversion.match(array)

        encoded = conversion.encode(array)
        assert isinstance(encoded, bytes)

        decoded = conversion.decode(encoded)
        assert np.all(array == decoded)
