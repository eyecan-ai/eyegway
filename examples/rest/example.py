from redis.asyncio import Redis
from redis.asyncio.client import Pipeline
import eyegway.hubs as amc
import eyegway.communication as ecom
import eyegway.packaging as emp
import fastapi as fa
import fastapi.responses as far
import typing as t
import uvicorn


class MessageHubServer(fa.FastAPI):

    def __init__(self):
        super().__init__()
        self._message_hubs_map: t.Dict[str, amc.AsyncMessageHub] = {}

        self.get("/message-hub/{name}/history_size")(self.history_size)
        self.get("/message-hub/{name}/buffer_size")(self.buffer_size)
        self.get("/message-hub/{name}/pop", response_model=bytes)(self.pop)
        self.get("/message-hub/{name}/last", response_model=bytes)(self.last)
        self.post("/message-hub/{name}/clear_buffer")(self.clear_buffer)
        self.post("/message-hub/{name}/clear_history")(self.clear_history)

    async def clear_buffer(self, name: str) -> None:
        if name not in self._message_hubs_map:
            return

        hub = self._message_hubs_map[name]
        await hub.clear_buffer()

    async def clear_history(self, name: str) -> None:
        if name not in self._message_hubs_map:
            return

        hub = self._message_hubs_map[name]
        await hub.clear_history()

    async def history_size(self, name: str) -> int:
        if name not in self._message_hubs_map:
            self._message_hubs_map[name] = amc.AsyncMessageHub.create(name=name)

        hub = self._message_hubs_map[name]
        return await hub.history_size()

    async def buffer_size(self, name: str) -> int:
        if name not in self._message_hubs_map:
            self._message_hubs_map[name] = amc.AsyncMessageHub.create(name=name)

        hub = self._message_hubs_map[name]
        return await hub.buffer_size()

    async def pop(self, name: str, timeout: int = 1) -> bytes:
        if timeout < 1:
            timeout = 1
        if name not in self._message_hubs_map:
            self._message_hubs_map[name] = amc.AsyncMessageHub.create(name=name)

        hub = self._message_hubs_map[name]
        data = await hub.pop(timeout)
        if data is None:
            return far.Response(None, status_code=204)
        return far.Response(
            await hub.pop_raw(timeout),
            media_type="application/octet-stream",
        )

    async def last(self, name: str, offset: int = 0) -> bytes:
        if name not in self._message_hubs_map:
            self._message_hubs_map[name] = amc.AsyncMessageHub.create(name=name)

        hub = self._message_hubs_map[name]
        data = await hub.last(offset)
        if data is None:
            return far.Response(None, status_code=204)
        return far.Response(
            await hub.last_raw(offset),
            media_type="application/octet-stream",
        )


if __name__ == "__main__":
    app = MessageHubServer()
    uvicorn.run(app, host="0.0.0.0", port=8000)
