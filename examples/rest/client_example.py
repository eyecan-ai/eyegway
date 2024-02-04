import asyncio
import eyegway.rest.hubs as erh
import rich
import numpy as np
import httpx
import eyegway.packers.factory as epf
import eyegway.rest.hubs as erh
import pydantic as pyd
import typing as t


class HubsRestAPIClientAsync(pyd.BaseModel):
    host: str = "0.0.0.0"
    port: int = erh.HUBS_REST_API_DEFAULT_PORT

    async def history_size(self, name: str) -> int:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{self.host}:{self.port}/hubs/{name}/history_size"
            )
            return response.json()

    async def buffer_size(self, name: str) -> int:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{self.host}:{self.port}/hubs/{name}/buffer_size"
            )
            return response.json()

    async def clear_history(self, name: str) -> None:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"http://{self.host}:{self.port}/hubs/{name}/clear_history"
            )

    async def clear_buffer(self, name: str) -> None:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"http://{self.host}:{self.port}/hubs/{name}/clear_buffer"
            )

    async def last_raw(self, name: str, offset: int = 0) -> t.Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{self.host}:{self.port}/hubs/{name}/last?offset={offset}"
            )
            return response.content

    async def last(self, name: str, offset: int = 0) -> t.Any:
        raw_data = await self.last_raw(name, offset)
        unpacked = epf.PackersFactory.default().unpack(raw_data)
        return unpacked

    async def pop_raw(self, name: str, timeout: int = 1) -> t.Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{self.host}:{self.port}/hubs/{name}/pop?timeout={timeout}"
            )
            if response.status_code == 204:
                return None
            return response.content

    async def pop(self, name: str, timeout: int = 1) -> t.Any:
        raw_data = await self.pop_raw(name, timeout)
        if raw_data is None:
            return None
        unpacked = epf.PackersFactory.default().unpack(raw_data)
        return unpacked

    async def push(self, name: str, data: t.Any) -> None:
        packed = epf.PackersFactory.default().pack(data)
        async with httpx.AsyncClient() as client:
            await client.post(
                f"http://{self.host}:{self.port}/hubs/{name}/push", data=packed
            )


async def run():
    client = HubsRestAPIClientAsync()
    hub_name = "client_example"

    await client.clear_buffer(hub_name)
    await client.clear_history(hub_name)

    rich.print(f"Hub |[#00aa22]{hub_name}[/]|")
    rich.print("History Size:", await client.history_size(hub_name))
    rich.print("Buffer Size:", await client.buffer_size(hub_name))

    rich.print("Pushing ...")
    for idx in range(10):
        data = {
            "time": idx,
            "command": f"SampleCommand_{idx}",
            "data": np.random.uniform(0, 1, (4,)),
        }
        await client.push(hub_name, data)

    rich.print(f"Hub |[#00aa22]{hub_name}[/]|")
    rich.print("History Size:", await client.history_size(hub_name))
    rich.print("Buffer Size:", await client.buffer_size(hub_name))

    rich.print("Popping ...")
    while True:
        data = await client.pop(hub_name)
        rich.print(data)
        if data is None:
            break

    rich.print(f"Hub |[#00aa22]{hub_name}[/]|")
    rich.print("History Size:", await client.history_size(hub_name))
    rich.print("Buffer Size:", await client.buffer_size(hub_name))

    history_size = await client.history_size(hub_name)

    last_data = [
        (await client.last(hub_name, idx))['time'] for idx in range(history_size)
    ]
    rich.print("Last Data:", last_data)


if __name__ == "__main__":
    asyncio.run(run())
