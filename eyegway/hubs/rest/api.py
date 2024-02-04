import eyegway.hubs.asyn as eha
import eyegway.hubs as eh
import fastapi as fa
import fastapi.responses as far
import fastapi.requests as farq
import typing as t
import fastapi.middleware.cors as fa_cors

HUBS_REST_API_DEFAULT_PORT = 55221


class HubsRestAPI(fa.FastAPI):

    def __init__(self, config: t.Optional[eh.HubsConfig] = None):
        super().__init__()
        self.config = config
        self._message_hubs_map: t.Dict[str, eha.AsyncMessageHub] = {}

        self.add_middleware(
            fa_cors.CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.get("/hubs/{name}/history_size")(self.history_size)
        self.get("/hubs/{name}/buffer_size")(self.buffer_size)
        self.get("/hubs/{name}/pop", response_model=bytes)(self.pop)
        self.get("/hubs/{name}/last", response_model=bytes)(self.last)
        self.post("/hubs/{name}/clear_buffer")(self.clear_buffer)
        self.post("/hubs/{name}/clear_history")(self.clear_history)
        self.post("/hubs/{name}/push")(self.push)

    def get_hub(self, name: str) -> eha.AsyncMessageHub:
        if name not in self._message_hubs_map:
            self._message_hubs_map[name] = eha.AsyncMessageHub.create(
                name=name, config=self.config
            )
        return self._message_hubs_map[name]

    async def clear_buffer(self, name: str) -> None:
        hub = self.get_hub(name)
        await hub.clear_buffer()

    async def clear_history(self, name: str) -> None:
        hub = self.get_hub(name)
        await hub.clear_history()

    async def history_size(self, name: str) -> int:
        hub = self.get_hub(name)
        return await hub.history_size()

    async def buffer_size(self, name: str) -> int:
        hub = self.get_hub(name)
        return await hub.buffer_size()

    async def pop(self, name: str, timeout: int = 1) -> bytes:
        if timeout < 1:
            timeout = 1
        hub = self.get_hub(name)
        data = await hub.pop_raw(timeout)
        if data is None:
            return far.Response(None, status_code=204)

        return far.Response(data, media_type="application/octet-stream")

    async def last(self, name: str, offset: int = 0) -> bytes:
        hub = self.get_hub(name)
        data = await hub.last_raw(offset)
        if data is None:
            return far.Response(None, status_code=204)

        return far.Response(data, media_type="application/octet-stream")

    async def push(self, name: str, request: farq.Request) -> None:
        hub = self.get_hub(name)
        data = await request.body()
        await hub.push_raw(data)
