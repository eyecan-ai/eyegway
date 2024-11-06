import typing as t
from abc import ABC, abstractmethod
from collections import deque

import pydantic as pyd

from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.sync import MessageHub


class HubView(ABC, pyd.BaseModel):
    """
    An abstract base class for views that rearrange elements into a dictionary format.

    Attributes:
        Config (class): Configuration class for Pydantic model.
    """

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def _rearrange(self, elements: list) -> t.Dict[str, t.Any]:
        """
        Rearranges a list of elements into a dictionary.

        Args:
            elements (list): A list of elements to be rearranged.

        Returns:
            Dict[str, Any]: A dictionary where keys are string indices and values
                                are the elements.
        """
        pass

    def view(self, hub: MessageHub) -> t.Dict[str, t.Any]:
        """
        Provides a view of the elements of a sync hub by rearranging them.

        Args:
            elements (list): A list of elements to be viewed.

        Returns:
            Dict[str, Any]: A dictionary where keys are string indices and values
                                are rearrangement of the elements.
        """

        elements = hub.last_multiple(0, hub.history_size())
        return self._rearrange(elements)

    async def view_async(self, hub: AsyncMessageHub) -> t.Dict[str, t.Any]:
        """
        Provides a view of the elements of an async hub by rearranging them.

        Args:
            elements (list): A list of elements to be viewed.

        Returns:
            Dict[str, Any]: A dictionary where keys are string indices and values
                                are rearrangement of the elements.
        """

        elements = await hub.last_multiple(0, await hub.history_size())
        return self._rearrange(elements)


class SequentialDictView(HubView):
    """
    A view that rearranges elements into a dictionary with sequential keys.

    Inherits from HubView and overrides the _rearrange method to arrange elements
        in sequential order.

    Example:
        elements = ['a', 'b', 'c']
        view = SequentialDictView()
        result = view.view(elements)
        result -> {'0': 'a', '1': 'b', '2': 'c'}
    """

    def _rearrange(self, elements: list) -> t.Dict[str, t.Any]:
        return {str(i): element for i, element in enumerate(elements)}


class ReverseSequentialDictView(HubView):
    """
    A view that rearranges elements into a dictionary with sequential keys
            in reverse order.

    Inherits from HubView and overrides the _rearrange method to arrange
            elements in reverse order.

    Example:
        elements = ['a', 'b', 'c']
        view = ReverseSequentialDictView()
        result = view.view(elements)
        result -> {'0': 'c', '1': 'b', '2': 'a'}
    """

    def _rearrange(self, elements: list) -> t.Dict[str, t.Any]:
        return {str(i): element for i, element in enumerate(elements[::-1])}


class ValueAccumulatorView(HubView):
    """
    A view that accumulates values from nested dictionaries based on specified keys.

    Attributes:
        keys (List[str]): A list of dot notation keys used to extract values from
                            nested dictionaries.

    Example:
        elements = [
            {'a': {'b': 1}},
            {'a': {'b': 2}},
            {'a': {'b': 3}}
        ]
        view = ValueAccumulatorView(keys=['a.b'])
        result = view.view(elements)
        result -> {'a': {b': [1, 2, 3]}}
    """

    keys: t.List[str] = pyd.Field(..., description="Keys")

    def _get_value(self, data: t.Dict[str, t.Any], dotted_key: str) -> t.Any:
        """
        Retrieves the value from a nested dictionary using a dot notation key.

        Args:
            data (Dict[str, Any]): The dictionary to retrieve the value from.
            dotted_key (str): The dot notation key to access the nested value.

        Returns:
            Any: The value corresponding to the dotted key, or None if the key
                    does not exist.
        """
        keys = dotted_key.split(".")
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    def _set_value(
        self, data: t.Dict[str, t.Any], dotted_key: str, value: t.Any
    ) -> None:
        """
        Sets the value in a nested dictionary using a dot notation key.

        Args:
            data (Dict[str, Any]): The dictionary to set the value in.
            dotted_key (str): The dot notation key to access the nested location.
            value (Any): The value to set at the specified location.
        """
        keys = dotted_key.split(".")
        for key in keys[:-1]:
            if key not in data or not isinstance(data[key], dict):
                data[key] = {}
            data = data[key]
        data[keys[-1]] = value

    def _rearrange(self, elements: list) -> t.Dict[str, t.Any]:
        """
        Rearranges a list of elements into a dictionary of accumulated values.

        This method processes a list of elements, extracting values based on the keys
        defined in the `keys` attribute. It accumulates these values in a dictionary,
        where each key corresponds to a list of values extracted from the elements.

        Args:
            elements (list): A list of dictionaries from which values will be extracted.

        Returns:
            Dict[str, Any]: A dictionary where each key corresponds to a list of
                                accumulated values.
        """
        accumulated_data: t.Dict[str, t.Any] = {}
        for key in self.keys:
            values = deque()
            for element in elements:
                value = self._get_value(element, key)
                if value is not None:
                    values.append(value)
            self._set_value(accumulated_data, key, list(values))
        return accumulated_data
