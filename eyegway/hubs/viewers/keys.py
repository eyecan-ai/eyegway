import typing as t
from collections import deque

import pydantic as pyd

from eyegway.hubs.viewers import HubView


class KeysView(HubView):
    keys: t.List[str] = pyd.Field(..., description="Keys")

    def _get_value(self, data: t.Dict[str, t.Any], dotted_key: str) -> t.Any:
        """
        Retrieves the value from a nested dictionary using a dot notation key.

        Args:
            data (Dict[str, Any]): The dictionary to retrieve the value from.
            dotted_key (str): The dot notation key to access the nested value.

        Returns:
            Any: The value corresponding to the dotted key, or None if the key does not exist.
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
        accumulated_data: t.Dict[str, t.Any] = {}
        for key in self.keys:
            values = deque()
            for element in elements[::-1]:
                value = self._get_value(element, key)
                if value is not None:
                    values.append(value)
            self._set_value(accumulated_data, key, list(values))
        return accumulated_data
