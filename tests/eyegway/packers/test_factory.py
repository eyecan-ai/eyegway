import pytest
import numpy as np
import eyegway.packers.factory as epf
from deepdiff import DeepDiff
from .commons import test_valid_messages, test_invalid_messages


class TestPackersFactory:

    @pytest.mark.parametrize("message", test_valid_messages())
    def test_packer_smart_images(self, message):
        pickpacker = epf.PackersFactory.create("smart_images")
        packed = pickpacker.pack(message)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)
        assert not DeepDiff(message, unpacked, exclude_types=[np.ndarray])

    @pytest.mark.parametrize("message", test_valid_messages())
    def test_packer_raw(self, message):
        pickpacker = epf.PackersFactory.create("raw")
        packed = pickpacker.pack(message)
        assert len(packed) > 0
        unpacked = pickpacker.unpack(packed)
        assert not DeepDiff(message, unpacked)

    @pytest.mark.parametrize("message", test_invalid_messages())
    def test_packer_raw_with_invalid_message(self, message):
        pickpacker = epf.PackersFactory.create("raw")

        with pytest.raises(TypeError):
            pickpacker.pack(message)
