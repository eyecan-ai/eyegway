import numpy as np
import pytest
from deepdiff import DeepDiff

import eyegway.packers.factory as epf

from .commons import invalid_messages, valid_messages


class TestPackersFactory:

    @pytest.mark.parametrize("message", valid_messages())
    def test_packer_smart_images(self, message):
        pickpacker = epf.PackersFactory.create("smart_images")
        packed = pickpacker.pack(message)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)
        assert not DeepDiff(message, unpacked, exclude_types=[np.ndarray])

    @pytest.mark.parametrize("message", valid_messages())
    def test_packer_raw(self, message):
        pickpacker = epf.PackersFactory.create("raw")
        packed = pickpacker.pack(message)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)
        assert not DeepDiff(message, unpacked)

    @pytest.mark.parametrize("message", valid_messages())
    def test_packer_default(self, message):
        pickpacker = epf.PackersFactory.default()
        packed = pickpacker.pack(message)
        assert len(packed) > 0
        # Givne that default packer can change, we can only check that it can be
        # unpacked
        unpacked = pickpacker.unpack(packed)
        pickpacker.pretty_print(unpacked)

    @pytest.mark.parametrize("message", invalid_messages())
    def test_packer_raw_with_invalid_message(self, message):
        pickpacker = epf.PackersFactory.create("raw")

        with pytest.raises(TypeError):
            pickpacker.pack(message)
