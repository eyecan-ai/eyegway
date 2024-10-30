import typing as t
from abc import ABC

import pydantic as pyd


class HubView(ABC, pyd.BaseModel):

    class Config:
        arbitrary_types_allowed = True

    def _rearrange(self, elements: list) -> t.Dict[str, t.Any]:
        return {str(i): element for i, element in enumerate(elements)}

    def view(self, elements: list) -> t.Dict[str, t.Any]:
        return self._rearrange(elements)


class ReverseView(HubView):
    def _rearrange(self, elements: list) -> t.Dict[str, t.Any]:
        return {str(i): element for i, element in enumerate(elements[::-1])}
