from unittest.mock import MagicMock

import pytest

from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.sync import MessageHub
from eyegway.hubs.viewers import (
    ReverseSequentialDictView,
    SequentialDictView,
    ValueAccumulatorView,
)


class TestSequentialDictView:

    def test_empty_list(self):
        view = SequentialDictView()
        hub = MagicMock(spec=MessageHub)
        hub.last_multiple.return_value = []
        hub.history_size.return_value = 0
        result = view._sync_view(hub)
        assert result == {}

    def test_list_of_elements(self):
        view = SequentialDictView()
        hub = MagicMock(spec=MessageHub)
        elements = ["a", "b", "c"]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = view._sync_view(hub)
        assert result == {"0": "a", "1": "b", "2": "c"}

    def test_nested_data(self):
        view = SequentialDictView()
        hub = MagicMock(spec=MessageHub)
        elements = [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = view._sync_view(hub)
        assert result == {
            "0": {"key1": "value1"},
            "1": {"key2": "value2"},
            "2": {"key3": "value3"},
        }

    @pytest.mark.asyncio
    async def test_empty_list_async(self):
        view = SequentialDictView()
        hub = MagicMock(spec=AsyncMessageHub)
        hub.last_multiple.return_value = []
        hub.history_size.return_value = 0
        result = await view._async_view(hub)
        assert result == {}

    @pytest.mark.asyncio
    async def test_list_of_elements_async(self):
        view = SequentialDictView()
        hub = MagicMock(spec=AsyncMessageHub)
        elements = ["a", "b", "c"]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = await view._async_view(hub)
        assert result == {"0": "a", "1": "b", "2": "c"}

    @pytest.mark.asyncio
    async def test_nested_data_async(self):
        view = SequentialDictView()
        hub = MagicMock(spec=AsyncMessageHub)
        elements = [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = await view._async_view(hub)
        assert result == {
            "0": {"key1": "value1"},
            "1": {"key2": "value2"},
            "2": {"key3": "value3"},
        }


class TestReverseSequentialDictView:

    def test_empty_list(self):
        view = ReverseSequentialDictView()
        hub = MagicMock(spec=MessageHub)
        hub.last_multiple.return_value = []
        hub.history_size.return_value = 0
        result = view._sync_view(hub)
        assert result == {}

    def test_list_of_elements(self):
        view = ReverseSequentialDictView()
        hub = MagicMock(spec=MessageHub)
        elements = ["a", "b", "c"]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = view._sync_view(hub)
        assert result == {"0": "c", "1": "b", "2": "a"}

    def test_nested_data(self):
        view = ReverseSequentialDictView()
        hub = MagicMock(spec=MessageHub)
        elements = [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = view._sync_view(hub)
        assert result == {
            "0": {"key3": "value3"},
            "1": {"key2": "value2"},
            "2": {"key1": "value1"},
        }

    @pytest.mark.asyncio
    async def test_empty_list_async(self):
        view = ReverseSequentialDictView()
        hub = MagicMock(spec=AsyncMessageHub)
        hub.last_multiple.return_value = []
        hub.history_size.return_value = 0
        result = await view._async_view(hub)
        assert result == {}

    @pytest.mark.asyncio
    async def test_list_of_elements_async(self):
        view = ReverseSequentialDictView()
        hub = MagicMock(spec=AsyncMessageHub)
        elements = ["a", "b", "c"]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = await view._async_view(hub)
        assert result == {"0": "c", "1": "b", "2": "a"}

    @pytest.mark.asyncio
    async def test_nested_data_async(self):
        view = ReverseSequentialDictView()
        hub = MagicMock(spec=AsyncMessageHub)
        elements = [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}]
        hub.last_multiple.return_value = elements
        hub.history_size.return_value = 0
        result = await view._async_view(hub)
        assert result == {
            "0": {"key3": "value3"},
            "1": {"key2": "value2"},
            "2": {"key1": "value1"},
        }


class TestValueAccumulatorView:

    @pytest.fixture
    def view(self) -> ValueAccumulatorView:
        return ValueAccumulatorView(keys=["a.b", "c.d.e"])

    def test_get_value_simple(self, view: ValueAccumulatorView):
        data = {"a": {"b": 1}}
        assert view._get_value(data, "a.b") == 1

    def test_get_value_non_existent_key(self, view: ValueAccumulatorView):
        data = {"a": {"b": 1}}
        assert view._get_value(data, "a.c") is None

    def test_get_value_deeply_nested(self, view: ValueAccumulatorView):
        data = {"a": {"b": {"c": {"d": 2}}}}
        assert view._get_value(data, "a.b.c.d") == 2

    def test_set_value_simple(self, view: ValueAccumulatorView):
        data = {}
        view._set_value(data, "a.b", 1)
        assert data == {"a": {"b": 1}}

    def test_set_value_deeply_nested(self, view: ValueAccumulatorView):
        data = {}
        view._set_value(data, "a.b.c.d", 2)
        assert data == {"a": {"b": {"c": {"d": 2}}}}

    def test_set_value_creates_dict(self, view: ValueAccumulatorView):
        data = {"a": 1}
        view._set_value(data, "a.b", 2)
        assert data == {"a": {"b": 2}}

        data = {"a": {"b": 1}}
        view._set_value(data, "a.b.c", 3)
        assert data == {"a": {"b": {"c": 3}}}

    def test_rearrange_empty(self, view: ValueAccumulatorView):
        elements = []
        result = view._rearrange(elements)
        assert result == {"a": {"b": []}, "c": {"d": {"e": []}}}

    def test_rearrange_nested(self, view: ValueAccumulatorView):
        elements = [
            {"a": {"b": 1}, "c": {"d": {"e": 2}}},
            {"a": {"b": 3}, "c": {"d": {"e": 4}}},
            {"a": {"b": 5}, "c": {"d": {"e": 6}}},
        ]
        result = view._rearrange(elements)
        assert result == {"a": {"b": [1, 3, 5]}, "c": {"d": {"e": [2, 4, 6]}}}

    def test_rearrange_with_missing_keys(self, view: ValueAccumulatorView):
        elements = [
            {"a": {"b": 1}},
            {"c": {"d": {"e": 2}}},
            {"a": {"b": 3}, "c": {"d": {"e": 4}}},
        ]
        result = view._rearrange(elements)
        assert result == {"a": {"b": [1, 3]}, "c": {"d": {"e": [2, 4]}}}
