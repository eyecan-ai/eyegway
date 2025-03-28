import numpy as np
import asyncio
import typing as t
import eyegway.hubs as eh
import eyegway.hubs.connectors as ehc
import eyegway.hubs.asyn as eha
import eyegway.utils as eut
import eyegway.hubs.connectors.pipelime as ehcp
import pipelime.stages as pst
import pipelime.sequences as pls
import pipelime.items as pli
import pydantic as pyd
from abc import ABC, abstractmethod
import cv2
import pipelime.stages as pst


class StageDrawing(pst.SampleStage):

    def __call__(self, x: pls.Sample) -> pls.Sample:
        image = x['backl_image']()
        h, w = image.shape[:2]

        # draw random circles with opencv
        for i in range(10):
            cx = np.random.randint(0, w)
            cy = np.random.randint(0, h)
            radius = np.random.randint(0, 100)
            color = (
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                np.random.randint(0, 255),
            )
            cv2.circle(image, (cx, cy), radius, color, -1)
        return x.set_value('backl_image', image)


class HubBridgeAsync(pyd.BaseModel, ABC):
    hub_from: str
    hub_to: str
    hub_from_connectors: t.List[ehc.HubConnector] = []
    hub_to_connectors: t.List[ehc.HubConnector] = []
    clear_hub_to: bool = True

    model_config = pyd.ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def process(self, data: t.Any) -> t.Any:
        pass

    async def run(self):
        start_hub = eha.AsyncMessageHub.create(self.hub_from)
        end_hub = eha.AsyncMessageHub.create(self.hub_to)

        start_hub.connectors.extend(self.hub_from_connectors)
        end_hub.connectors.extend(self.hub_to_connectors)

        if self.clear_hub_to:
            await end_hub.clear()

        while True:
            data = await start_hub.pop(timeout=0)
            data = self.process(data)
            await end_hub.push(data)


class MyBridge(HubBridgeAsync):
    hub_from: str = "osella"
    hub_to: str = "osella2"
    hub_from_connectors: t.List[ehc.HubConnector] = [ehcp.PipelimeHubConnector()]
    hub_to_connectors: t.List[ehc.HubConnector] = [ehcp.PipelimeHubConnector()]

    def process(self, data: t.Any) -> t.Any:
        stage = StageDrawing()
        data = stage(data)
        # print(type(data))
        # image = data['backl_image']()
        # h, w = image.shape[:2]

        # # draw random circles with opencv
        # for i in range(10):
        #     x = np.random.randint(0, w)
        #     y = np.random.randint(0, h)
        #     radius = np.random.randint(0, 100)
        #     color = (
        #         np.random.randint(0, 255),
        #         np.random.randint(0, 255),
        #         np.random.randint(0, 255),
        #     )
        #     cv2.circle(image, (x, y), radius, color, -1)

        return data


if __name__ == '__main__':

    bridge = MyBridge()
    asyncio.run(bridge.run())
