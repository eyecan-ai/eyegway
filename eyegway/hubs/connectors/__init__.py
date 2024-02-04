import typing as t


class HubConnector:

    def world_to_hub(self, data: t.Any) -> t.Any:
        return data

    def hub_to_world(self, data: t.Any) -> t.Any:
        return data
