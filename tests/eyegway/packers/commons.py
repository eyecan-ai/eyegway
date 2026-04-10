import typing as t

import numpy as np
import pydantic as pyd


def simple_messages():
    return [
        "Hello, world!",
        1,
        4.312312321312312312,
        [1, 2, 3],
        [2.3, 2, [2, 3]],
        {"a": 1, "b": 2, "c": 3},
        {"list": [1, 2, 3]},
        {
            "metadata": {
                "alpha": 1,
                2: "hello",
                True: False,
                2.2: "float",
            }
        },
    ]


def numpy_messages():
    return [
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


def valid_numpy_messages() -> list[t.Any]:
    return simple_messages() + numpy_messages()


def valid_messages() -> list[t.Any]:
    return valid_numpy_messages() + []


# Invalid messages


class InvalidObject(pyd.BaseModel):
    a: int = 2


def invalid_messages() -> list[t.Any]:
    return [InvalidObject()]
