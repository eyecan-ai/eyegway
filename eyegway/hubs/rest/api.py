import typing as t

import fastapi as fa
import fastapi.middleware.cors as fa_cors
import fastapi.requests as farq
import fastapi.responses as far
import pydantic as pyd

import eyegway.hubs as eh
import eyegway.hubs.asyn as eha

HUBS_REST_API_DEFAULT_PORT = 55221


class VariableValue(pyd.BaseModel):
    value: t.Any


class HubsRestAPI(fa.FastAPI):
    def __init__(
        self,
        config: eh.HubsConfig | None = None,
        root_path: str | None = None,
    ):
        super().__init__(root_path=root_path)
        self.config = config
        self._message_hubs_map: dict[str, eha.AsyncMessageHub] = {}
        self._message_hubs_manager = eha.AsyncMessageHubManager.create(config=config)

        self.add_middleware(
            fa_cors.CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.get(
            "/health",
            summary="Health check",
            responses={
                fa.status.HTTP_200_OK: {"description": "Ready to serve requests"},
                fa.status.HTTP_503_SERVICE_UNAVAILABLE: {
                    "description": "Not ready, retry later"
                },
            },
        )(self.health_check)

        self.get("/hubs")(self.hubs_list)
        self.get("/hubs/{name}/history_size")(self.history_size)
        self.get("/hubs/{name}/buffer_size")(self.buffer_size)
        self.get("/hubs/{name}/pop", response_model=bytes)(self.pop)
        self.get("/hubs/{name}/last", response_model=bytes)(self.last)
        self.get("/hubs/{name}/history_frozen")(self.history_frozen)
        self.get("/hubs/{name}/buffer_frozen")(self.buffer_frozen)
        self.post("/hubs/{name}/clear_buffer")(self.clear_buffer)
        self.post("/hubs/{name}/clear_history")(self.clear_history)
        self.post("/hubs/{name}/push")(self.push)
        self.post("/hubs/{name}/freeze_buffer")(self.freeze_buffer)
        self.post("/hubs/{name}/freeze_history")(self.freeze_history)
        self.post("/hubs/{name}/unfreeze_buffer")(self.unfreeze_buffer)
        self.post("/hubs/{name}/unfreeze_history")(self.unfreeze_history)
        self.get("/hubs/{name}/variables/{variable}")(self.get_variable_value)
        self.post("/hubs/{name}/variables/{variable}")(self.set_variable_value)
        self.delete("/hubs/{name}/variables/{variable}")(self.delete_variable)
        self.get("/hubs/{name}/variables")(self.list_variables)

    async def health_check(self, response: fa.Response):
        try:
            ready = self._message_hubs_manager.redis.ping()
        except Exception:
            ready = False

        response.status_code = (
            fa.status.HTTP_200_OK if ready else fa.status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def get_hub(self, name: str) -> eha.AsyncMessageHub:
        if name not in self._message_hubs_map:
            self._message_hubs_map[name] = eha.AsyncMessageHub.create(
                name=name, config=self.config, redis=self._message_hubs_manager.redis
            )
        return self._message_hubs_map[name]

    async def hubs_list(self) -> list[str]:
        return await self._message_hubs_manager.list()

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

    async def pop(self, name: str, timeout: float = 1) -> far.Response:
        timeout = max(timeout, 1)
        hub = self.get_hub(name)
        data = await hub.pop_raw(timeout)
        if data is None:
            return far.Response(None, status_code=204)

        return far.Response(data, media_type="application/octet-stream")

    async def last(self, name: str, offset: int = 0) -> far.Response:
        hub = self.get_hub(name)
        data = await hub.last_raw(offset)
        if data is None:
            return far.Response(None, status_code=204)

        return far.Response(data, media_type="application/octet-stream")

    async def push(self, name: str, request: farq.Request) -> None:
        hub = self.get_hub(name)
        data = await request.body()
        await hub.push_raw(data)

    async def history_frozen(self, name: str) -> bool:
        hub = self.get_hub(name)
        return await hub.is_history_frozen()

    async def buffer_frozen(self, name: str) -> bool:
        hub = self.get_hub(name)
        return await hub.is_buffer_frozen()

    async def freeze_buffer(self, name: str) -> None:
        hub = self.get_hub(name)
        await hub.freeze_buffer()

    async def freeze_history(self, name: str) -> None:
        hub = self.get_hub(name)
        await hub.freeze_history()

    async def unfreeze_buffer(self, name: str) -> None:
        hub = self.get_hub(name)
        await hub.freeze_buffer(False)

    async def unfreeze_history(self, name: str) -> None:
        hub = self.get_hub(name)
        await hub.freeze_history(False)

    async def get_variable_value(self, name: str, variable: str) -> t.Any:
        hub = self.get_hub(name)
        return await hub.get_variable_value(variable)

    async def set_variable_value(
        self,
        name: str,
        variable: str,
        value: VariableValue,
    ) -> None:
        hub = self.get_hub(name)
        await hub.set_variable_value(variable, value.value)

    async def delete_variable(self, name: str, variable: str) -> None:
        hub = self.get_hub(name)
        await hub.delete_variable(variable)

    async def list_variables(self, name: str) -> list[str]:
        hub = self.get_hub(name)
        return await hub.list_variables(include_privates=False)
