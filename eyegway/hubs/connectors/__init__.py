import typing as t
from abc import ABC, abstractmethod


class HubConnector(ABC):

    @abstractmethod
    def world_to_hub(self, data: t.Any) -> t.Any:
        pass

    @abstractmethod
    def hub_to_world(self, data: t.Any) -> t.Any:
        pass
