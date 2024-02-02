from abc import ABC, abstractmethod
import typing as t
import pickle


class Packer(ABC):
    @abstractmethod
    def pack(self, data: t.Any) -> bytes:
        pass

    @abstractmethod
    def unpack(self, buff: bytes) -> t.Any:
        pass


class PicklePacker(Packer):
    def pack(self, data: t.Any) -> bytes:
        return pickle.dumps(data)

    def unpack(self, buff: bytes) -> t.Any:
        return pickle.loads(buff)
