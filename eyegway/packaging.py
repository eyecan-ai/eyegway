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
import pydantic as pyd
import ast

MatchShape = t.Union[t.Sequence, type(Ellipsis)]
MatchDtype = t.Union[np.dtype, type(Ellipsis)]


class NumpyFormat(pyd.BaseModel, arbitrary_types_allowed=True):
    shape: MatchShape = pyd.Field(...)
    dtype: MatchDtype = pyd.Field(...)

    @pyd.validator('dtype', pre=True)
    def dtype_conversion(cls, v):
        return np.dtype(v) if v is not Ellipsis else v

    def __eq__(self, format: NumpyFormat) -> bool:
        return self.shape == format.shape and self.dtype == format.dtype

    def __str__(self) -> str:
        shape = (
            "..."
            if self.shape is Ellipsis
            else ",".join(["..." if x is Ellipsis else str(x) for x in self.shape])
        )
        dtype = self.dtype.name if self.dtype is not Ellipsis else "..."
        return f"({shape})/{dtype}"

    @classmethod
    def parse(cls, string: str) -> NumpyFormat:
        shape, dtype = string.split("/")
        shape = ast.literal_eval(shape)
        dtype = dtype.strip()
        dtype = np.dtype(dtype) if dtype != "..." else Ellipsis
        return NumpyFormat(shape=shape, dtype=dtype)

    def match(self, array: np.ndarray) -> bool:
        if self.shape is not ...:
            if len(array.shape) != len(self.shape):
                return False
            else:
                for i, s in enumerate(self.shape):
                    if s is not ... and array.shape[i] != s:
                        return False

        if self.dtype is not ...:
            if array.dtype != self.dtype:
                return False
        return True


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

    def __eq__(self, encoder: ImageEncoder) -> bool:
        return self.name() == encoder.name()


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


ImageEncodersMap = {
    TIFFImageEncoder.name(): TIFFImageEncoder(),
    PNGImageEncoder.name(): PNGImageEncoder(),
    JPEGImageEncoder.name(): JPEGImageEncoder(),
}


class ImageEncoderFactory:
    def __init__(self) -> None:
        self._encoders = {
            TIFFImageEncoder.name(): TIFFImageEncoder(),
            PNGImageEncoder.name(): PNGImageEncoder(),
            JPEGImageEncoder.name(): JPEGImageEncoder(),
        }

    def get(self, name: str) -> ImageEncoder:
        return self._encoders[name]


class NumpyConversion(pyd.BaseModel, arbitrary_types_allowed=True):
    numpy_format: NumpyFormat = pyd.Field(...)
    image_encoder: ImageEncoder = pyd.Field(...)

    def __eq__(self, conversion: NumpyConversion) -> bool:
        return (
            self.numpy_format == conversion.numpy_format
            and self.image_encoder == conversion.image_encoder
        )

    def __str__(self) -> str:
        return f"{str(self.numpy_format)}={self.image_encoder.name()}"

    @classmethod
    def parse(cls, string: str) -> NumpyConversion:
        numpy_format, encoder = string.split("=")
        numpy_format = NumpyFormat.parse(numpy_format)
        encoder = ImageEncodersMap.get(encoder.strip())
        return NumpyConversion(numpy_format=numpy_format, image_encoder=encoder)

    def match(self, array: np.ndarray) -> bool:
        return self.numpy_format.match(array)

    def encode(self, image: np.ndarray) -> bytes:
        return self.image_encoder.encode(image)

    def decode(self, buff: bytes) -> np.ndarray:
        return self.image_encoder.decode(buff)


class CustomMessageTypes(Enum):
    TENSOR = 66
    IMAGE = 67


class GenericMessageParser(ABC, pyd.BaseModel):
    @abstractmethod
    def match(self, obj) -> bool:
        pass

    @abstractmethod
    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        pass


class NumpyMessageParser(GenericMessageParser):
    numpy_conversions: t.List[NumpyConversion] = pyd.Field(default_factory=list)

    def match(self, obj) -> bool:
        return isinstance(obj, np.ndarray)

    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        for conversion in self.numpy_conversions:
            if conversion.numpy_format.match(obj):
                return msgpack.ExtType(
                    CustomMessageTypes.IMAGE.value,
                    msgpack.packb(
                        {
                            "shape": obj.shape,
                            "type": conversion.image_encoder.name(),
                            "data": conversion.image_encoder.encode(obj),
                        }
                    ),
                )

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


class MessageParserCompose(GenericMessageParser):
    parsers: t.List[GenericMessageParser] = pyd.Field(...)

    def match(self, obj) -> bool:
        for parser in self.parsers:
            if parser.match(obj):
                return True
        return False  # pragma: no cover

    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        for parser in self.parsers:
            if parser.match(obj):
                return parser(obj)
        return obj  # pragma: no cover


class GenericMessageUnparser(ABC, pyd.BaseModel):
    @abstractmethod
    def match(self, code: int) -> bool:
        pass

    @abstractmethod
    def __call__(self, code: int, data: bytes) -> t.Any:
        pass


class NumpyMessageUnparser(GenericMessageUnparser):

    def match(self, code: int) -> bool:
        return code in [CustomMessageTypes.TENSOR.value, CustomMessageTypes.IMAGE.value]

    def __call__(self, code: int, data: bytes) -> t.Any:
        if code == CustomMessageTypes.IMAGE.value:
            data = msgpack.unpackb(data, raw=False)
            encoder = ImageEncoderFactory().get(data["type"])
            shape = data["shape"]  # format check
            return encoder.decode(data["data"])
        else:
            data = msgpack.unpackb(data, raw=False)
            return np.frombuffer(data["data"], dtype=data["type"]).reshape(
                data["shape"]
            )


class MessageUnparserCompose(GenericMessageUnparser):
    unparsers: t.List[GenericMessageUnparser] = pyd.Field(...)

    def match(self, code: int) -> bool:
        for unparser in self.unparsers:
            if unparser.match(code):
                return True
        return False

    def __call__(self, code: int, data: bytes) -> t.Any:
        for unparser in self.unparsers:
            if unparser.match(code):
                return unparser(code, data)
        return data


class MessagePacker(pyd.BaseModel, arbitrary_types_allowed=True):
    parser: MessageParserCompose = pyd.Field(...)
    unparser: MessageUnparserCompose = pyd.Field(...)
    _packer: msgpack.Packer = pyd.PrivateAttr()
    _unpacker: msgpack.Unpacker = pyd.PrivateAttr()

    # self._packer = msgpack.Packer(default=self._parser, use_bin_type=True)
    #     self._unpacker = msgpack.Unpacker(ext_hook=self._unparser, raw=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._packer = msgpack.Packer(default=self.parser, use_bin_type=True)
        self._unpacker = msgpack.Unpacker(ext_hook=self.unparser, raw=False)

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


def message_packer_smart_images() -> MessagePacker:
    conversions = [
        NumpyConversion(
            numpy_format=NumpyFormat(shape=(..., ..., 3), dtype=np.uint8),
            image_encoder=JPEGImageEncoder(),
        ),
        NumpyConversion(
            numpy_format=NumpyFormat(shape=(..., ...), dtype=np.uint8),
            image_encoder=PNGImageEncoder(),
        ),
    ]

    parser = MessageParserCompose(
        parsers=[NumpyMessageParser(numpy_conversions=conversions)]
    )

    unparser = MessageUnparserCompose(unparsers=[NumpyMessageUnparser()])

    return MessagePacker(parser=parser, unparser=unparser)


def message_packer_raw() -> MessagePacker:
    parser = MessageParserCompose(parsers=[NumpyMessageParser()])
    unparser = MessageUnparserCompose(unparsers=[NumpyMessageUnparser()])
    return MessagePacker(parser=parser, unparser=unparser)


############################################################################################################


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
