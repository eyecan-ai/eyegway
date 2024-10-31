import typing as t
from abc import ABC, abstractmethod

import pydantic as pyd


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

    def view(self, elements: list) -> t.Dict[str, t.Any]:
        """
        Provides a view of the elements by rearranging them.

        Args:
            elements (list): A list of elements to be viewed.

        Returns:
            Dict[str, Any]: A dictionary where keys are string indices and values
                                are rearrangement of the elements.
        """
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
