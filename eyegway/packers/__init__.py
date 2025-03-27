import pickle
import typing as t
from abc import ABC, abstractmethod
from enum import Enum

import msgpack
import numpy as np
import pydantic.v1 as pyd


class CustomMessageTypes(Enum):
    TENSOR = 66
    IMAGE = 67


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


class GenericMessageParser(ABC, pyd.BaseModel):
    @abstractmethod
    def match(self, obj) -> bool:
        pass

    @abstractmethod
    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        pass


class MessageParserCompose(GenericMessageParser):
    parsers: t.List[GenericMessageParser] = pyd.Field(...)

    def match(self, obj) -> bool:
        for parser in self.parsers:
            if parser.match(obj):
                return True
        return False  # pragma: no cover

    def __call__(self, obj) -> t.Union[msgpack.ExtType, t.Any]:
        if not self.match(obj):
            return obj
        for parser in self.parsers:
            if parser.match(obj):
                return parser(obj)
        return obj  # pragma: no cover


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


class GenericMessageUnparser(ABC, pyd.BaseModel):
    @abstractmethod
    def match(self, code: int) -> bool:
        pass

    @abstractmethod
    def __call__(self, code: int, data: bytes) -> t.Any:
        pass


class MessageUnparserCompose(GenericMessageUnparser):
    unparsers: t.List[GenericMessageUnparser] = pyd.Field(...)

    def match(self, code: int) -> bool:
        for unparser in self.unparsers:
            if unparser.match(code):
                return True
        return False  # pragma: no cover

    def __call__(self, code: int, data: bytes) -> t.Any:
        for unparser in self.unparsers:
            if unparser.match(code):
                return unparser(code, data)
        return data  # pragma: no cover


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


class Packer(ABC):
    @abstractmethod
    def pack(self, data: t.Any) -> bytes:
        pass

    @abstractmethod
    def unpack(self, buff: bytes) -> t.Any:
        pass


class MessagePacker(Packer, pyd.BaseModel, arbitrary_types_allowed=True):
    parser: GenericMessageParser = pyd.Field()
    unparser: GenericMessageUnparser = pyd.Field()
    _packer: msgpack.Packer = pyd.PrivateAttr()
    _unpacker: msgpack.Unpacker = pyd.PrivateAttr()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._packer = msgpack.Packer(default=self.parser, use_bin_type=True)
        self._unpacker = msgpack.Unpacker(
            ext_hook=self.unparser,
            raw=False,
            strict_map_key=False,
        )

    def pack(self, obj) -> bytes:
        return self._packer.pack(obj)

    def unpack(self, buff: bytes) -> t.Any:
        self._unpacker.feed(buff)
        return self._unpacker.unpack()

    @classmethod
    def pretty_print(cls, data: t.Any, max_depth: int = 3):
        from rich import pretty

        def render_object(obj):
            if isinstance(obj, np.ndarray):
                return f"Array([{obj.shape}] {obj.dtype})"
            elif isinstance(obj, list):
                return [render_object(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: render_object(value) for key, value in obj.items()}
            else:
                return obj

        pretty.pprint(render_object(data), max_depth=max_depth)


class PicklePacker(Packer):
    def pack(self, data: t.Any) -> bytes:
        return pickle.dumps(data)

    def unpack(self, buff: bytes) -> t.Any:
        return pickle.loads(buff)
