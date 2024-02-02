from __future__ import annotations
import numpy as np
import io
import imageio.v3 as iio
import tifffile
import msgpack
import typing as t
from abc import ABC, abstractmethod, abstractclassmethod
from enum import Enum
import eyegway.commons as ecmn

MatchShape = t.Union[t.Sequence, type(Ellipsis)]
MatchDtype = t.Union[np.dtype, type(Ellipsis)]


def match_shape(
    array: np.ndarray,
    shape: MatchShape = ...,
    dtype: MatchDtype = ...,
):
    if shape is not ...:
        if len(array.shape) != len(shape):
            return False
        else:
            for i, s in enumerate(shape):
                if s is not ... and array.shape[i] != s:
                    return False

    if dtype is not ...:
        if array.dtype != dtype:
            return False
    return True


class ImageEncoder(ABC):
    @abstractmethod
    def encode(self, image: np.ndarray) -> bytes:
        pass

    @abstractmethod
    def decode(self, buff: bytes) -> np.ndarray:
        pass

    @abstractclassmethod
    def name(cls) -> str:
        pass


class TIFFImageEncoder(ImageEncoder):
    def encode(self, image: np.ndarray) -> bytes:
        buff = io.BytesIO()
        tifffile.imwrite(buff, image)
        return buff.getvalue()

    def decode(self, buff: bytes) -> np.ndarray:
        return tifffile.imread(io.BytesIO(buff))

    @classmethod
    def name(cls) -> str:
        return "image/tiff"


class PNGImageEncoder(ImageEncoder):
    def encode(self, image: np.ndarray) -> bytes:
        buff = io.BytesIO()
        iio.imwrite(buff, image, extension=".png")
        return buff.getvalue()

    def decode(self, buff: bytes) -> np.ndarray:
        return iio.imread(io.BytesIO(buff))

    @classmethod
    def name(cls) -> str:
        return "image/png"


class JPEGImageEncoder(ImageEncoder):
    def __init__(self, quality: int = 90):
        self._quality = quality

    def encode(self, image: np.ndarray) -> bytes:
        buff = io.BytesIO()
        iio.imwrite(buff, image, extension=".jpeg", **{"quality": self._quality})
        return buff.getvalue()

    def decode(self, buff: bytes) -> np.ndarray:
        return iio.imread(io.BytesIO(buff))

    @classmethod
    def name(cls) -> str:
        return "image/jpeg"


class ImageEncoderFactory:
    def __init__(self) -> None:
        self._encoders = {
            TIFFImageEncoder.name(): TIFFImageEncoder(),
            PNGImageEncoder.name(): PNGImageEncoder(),
            JPEGImageEncoder.name(): JPEGImageEncoder(),
        }

    def get(self, name: str) -> ImageEncoder:
        return self._encoders[name]


class CustomMessageTypes(Enum):
    TENSOR = 66
    IMAGE = 67


class CustomMessageParser(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def match(self, obj) -> bool:
        pass

    @abstractmethod
    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        pass


class NumpyToImageMessageParser(CustomMessageParser):
    def __init__(
        self,
        shape: MatchShape,
        dtype: MatchDtype,
        encoder: ImageEncoder,
    ) -> None:
        super().__init__()
        self._shape = shape
        self._dtype = np.dtype(dtype) if dtype is not Ellipsis else dtype
        self._encoder = encoder

    def match(self, obj) -> bool:
        if isinstance(obj, np.ndarray):
            return match_shape(obj, self._shape, self._dtype)
        return False  # pragma: no cover

    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        return msgpack.ExtType(
            CustomMessageTypes.IMAGE.value,
            msgpack.packb(
                {
                    "shape": obj.shape,
                    "type": self._encoder.name(),
                    "data": self._encoder.encode(obj),
                }
            ),
        )

    def __str__(self) -> str:
        """String representation of the parser like "(...,...,3) uint8 > image/jpg"
        so convert each Elliipsis to "..." and the dtype to its name"""

        if self._shape is Ellipsis:
            shape = "..."
        else:
            shape = ",".join(["..." if x is Ellipsis else str(x) for x in self._shape])
            shape = f'({shape})'
        dtype = self._dtype.name if self._dtype is not Ellipsis else "..."
        return f"{shape} {dtype} > {self._encoder.name()}"

    @classmethod
    def build(cls, string: str) -> NumpyToImageMessageParser:
        """Parse a string to a NumpyToImageMessageParser object,

        Examples:
            "...  uint8 > image/png"
            "(...,...,3) uint8 > image/jpg"

        Args:
            string (str): the string to parse

        Returns:
            NumpyToImageMessageParser: the parser object
        """
        import ast

        chunks = string.split(">")
        shapedtype, encoder = chunks[0].strip(), chunks[1].strip()
        shape, dtype = [x for x in shapedtype.split(" ") if x != ""]
        shape = ast.literal_eval(shape)
        dtype = np.dtype(dtype) if dtype != "..." else Ellipsis
        encoder = ImageEncoderFactory().get(encoder)
        return NumpyToImageMessageParser(shape, dtype, encoder)


class NumpyToTensorMessageParser(CustomMessageParser):
    def match(self, obj) -> bool:
        if isinstance(obj, np.ndarray):
            return True
        return False  # pragma: no cover

    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        return msgpack.ExtType(
            CustomMessageTypes.TENSOR.value,
            msgpack.packb(
                {
                    "shape": obj.shape,
                    "type": obj.dtype.name,
                    "data": obj.tobytes(),
                }
            ),
        )

    def __str__(self) -> str:
        return f"numpy2tensor"

    @classmethod
    def build(cls, string: str) -> NumpyToTensorMessageParser:
        string = string.strip()
        if string != "numpy2tensor":
            raise ValueError("Invalid string for NumpyToTensorMessageParser")
        return NumpyToTensorMessageParser()


class MultipleMessageParser(CustomMessageParser):
    REGISTERED_PARSERS = [
        NumpyToImageMessageParser,
        NumpyToTensorMessageParser,
    ]

    def __init__(self, parsers: t.List[CustomMessageParser] = []) -> None:
        super().__init__()
        self._parsers = parsers if len(parsers) > 0 else []  # handle clash

    @property
    def subparsers(self) -> t.List[CustomMessageParser]:
        return self._parsers

    def add(self, parser: CustomMessageParser):
        self._parsers.append(parser)

    def match(self, obj) -> bool:
        for parser in self._parsers:
            if parser.match(obj):
                return True
        return False  # pragma: no cover

    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        if self.match(obj):
            for parser in self._parsers:
                if parser.match(obj):
                    return parser(obj)
        return obj  # pragma: no cover

    def __str__(self) -> str:
        return " | ".join([str(parser) for parser in self._parsers])

    @classmethod
    def build(cls, string: str) -> MultipleMessageParser:
        parsers = []
        tokens = [x.strip() for x in string.split("|")]
        for token in tokens:
            for parser in cls.REGISTERED_PARSERS:
                try:
                    parsers.append(parser.build(token))
                except Exception as e:
                    pass

        built = MultipleMessageParser(parsers)
        return built


class CustomMessageUnparser(ABC):
    @abstractmethod
    def match(self, code: int) -> bool:
        pass

    @abstractmethod
    def __call__(self, code: int, data: bytes) -> t.Any:
        pass


class MultipleMessageUnparser(CustomMessageUnparser):
    def __init__(self, unparsers: t.Dict[int, CustomMessageUnparser] = {}) -> None:
        super().__init__()
        self._unparsers = unparsers if len(unparsers) > 0 else {}

    def add(self, code: int, unparser: CustomMessageUnparser):
        self._unparsers[code] = unparser

    def match(self, code: int) -> bool:
        for unparser in self._unparsers.values():
            if unparser.match(code):
                return True
        return False  # pragma: no cover

    def __call__(self, code: int, data: bytes) -> t.Any:
        if self.match(code):
            for unparser in self._unparsers.values():
                if unparser.match(code):
                    return unparser(code, data)
        return data  # pragma: no cover


class NumpyFromImageMessageUnparser(CustomMessageUnparser):
    def match(self, code: int) -> bool:
        return code == CustomMessageTypes.IMAGE.value

    def __call__(self, code: int, data: bytes) -> t.Any:
        data = msgpack.unpackb(data, raw=False)
        encoder = ImageEncoderFactory().get(data["type"])
        return encoder.decode(data["data"])


class NumpyFromTensorMessageUnparser(CustomMessageUnparser):
    def match(self, code: int) -> bool:
        return code == CustomMessageTypes.TENSOR.value

    def __call__(self, code: int, data: bytes) -> t.Any:
        data = msgpack.unpackb(data, raw=False)
        return np.frombuffer(data["data"], dtype=data["type"]).reshape(data["shape"])


class MsgPacker(ecmn.Packer):
    def __init__(
        self,
        parser: t.Optional[CustomMessageParser] = None,
        unparser: t.Optional[CustomMessageUnparser] = None,
    ):
        self._parser = parser
        self._unparser = unparser
        self._packer = msgpack.Packer(default=self._parser, use_bin_type=True)
        self._unpacker = msgpack.Unpacker(ext_hook=self._unparser, raw=False)

    def pack(self, obj) -> bytes:
        return self._packer.pack(obj)

    def unpack(self, buff: bytes) -> t.Any:
        self._unpacker.feed(buff)
        return self._unpacker.unpack()

    @classmethod
    def pretty_print(cls, data: t.Any):
        from rich import pretty

        np.set_printoptions(threshold=1, edgeitems=1, linewidth=100, suppress=True)
        pretty.install()
        pretty.pprint(data, max_string=10)


class DefaultMsgPacker(MsgPacker):
    DEFAULT_PARSERS_STRING = (
        '(...,...,3) uint8 > image/jpg | '
        + '(...,...) uint8 > image/png | '
        + 'numpy2tensor'
    )

    def __init__(self, parsers_string: t.Optional[str] = None) -> None:
        if parsers_string is None:
            parsers_string = self.DEFAULT_PARSERS_STRING
        super().__init__(
            parser=MultipleMessageParser.build(parsers_string),
            unparser=MultipleMessageUnparser(
                {
                    CustomMessageTypes.IMAGE.value: NumpyFromImageMessageUnparser(),
                    CustomMessageTypes.TENSOR.value: NumpyFromTensorMessageUnparser(),
                }
            ),
        )
