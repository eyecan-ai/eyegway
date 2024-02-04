from __future__ import annotations
import ast
import typing as t
import numpy as np
import pydantic as pyd
import msgpack
from eyegway.packers.images import ImageEncoder, ImageEncodersMap
from eyegway.packers import (
    CustomMessageTypes,
    GenericMessageParser,
    GenericMessageUnparser,
)

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


class NumpyMessageParser(GenericMessageParser):
    numpy_conversions: t.List[NumpyConversion] = pyd.Field(default_factory=list)

    def match(self, obj) -> bool:
        return isinstance(obj, np.ndarray)

    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        if not self.match(obj):
            return obj

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


class NumpyMessageUnparser(GenericMessageUnparser):

    def match(self, code: int) -> bool:
        return code in [CustomMessageTypes.TENSOR.value, CustomMessageTypes.IMAGE.value]

    def __call__(self, code: int, data: bytes) -> t.Any:
        if code == CustomMessageTypes.IMAGE.value:
            data = msgpack.unpackb(data, raw=False)
            encoder = ImageEncodersMap.get(data["type"])
            if 'shape' not in data:
                raise ValueError("Invalid image format, missing 'shape'")
            return encoder.decode(data["data"])
        else:
            data = msgpack.unpackb(data, raw=False)
            return np.frombuffer(data["data"], dtype=data["type"]).reshape(
                data["shape"]
            )
