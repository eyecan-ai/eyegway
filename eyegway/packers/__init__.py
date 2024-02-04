from abc import ABC, abstractmethod
from enum import Enum
import msgpack
import pydantic as pyd
import typing as t
import numpy as np


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
        if not self.match(code):
            return data  # pragma: no cover
        for unparser in self.unparsers:
            if unparser.match(code):
                return unparser(code, data)
        return data  # pragma: no cover


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄░▄▄▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


class MessagePacker(pyd.BaseModel, arbitrary_types_allowed=True):
    parser: MessageParserCompose = pyd.Field(...)
    unparser: MessageUnparserCompose = pyd.Field(...)
    _packer: msgpack.Packer = pyd.PrivateAttr()
    _unpacker: msgpack.Unpacker = pyd.PrivateAttr()

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
