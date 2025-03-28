from __future__ import annotations
import io
import tifffile
import imageio.v3 as iio
import numpy as np


from abc import ABC, abstractclassmethod, abstractmethod


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


ImageEncodersMap: dict[str, ImageEncoder] = {
    TIFFImageEncoder.name(): TIFFImageEncoder(),
    PNGImageEncoder.name(): PNGImageEncoder(),
    JPEGImageEncoder.name(): JPEGImageEncoder(),
}
