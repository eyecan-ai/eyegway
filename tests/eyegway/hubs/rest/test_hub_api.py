import eyegway.hubs.rest.api as erha
import eyegway.packers.factory as epf
import eyegway.hubs as eh
from httpx import AsyncClient
import pytest


class TestHubsRestAPI:

    @pytest.mark.asyncio
    async def test_lifecycle(self):
        api = erha.HubsRestAPI(config=eh.HubsConfig(redis_host="fakeredis"))
        packer = epf.PackersFactory.default()
        assert api is not None

        hub_name = "test"

        async with AsyncClient(app=api, base_url="http://test") as tc:

            response = await tc.post(f"/hubs/{hub_name}/clear_history")
            assert response.status_code == 200

            response = await tc.post(f"/hubs/{hub_name}/clear_buffer")
            assert response.status_code == 200

            response = await tc.get(f"/hubs/{hub_name}/history_size")
            assert response.status_code == 200
            assert response.json() == 0

            response = await tc.get(f"/hubs/{hub_name}/buffer_size")
            assert response.status_code == 200
            assert response.json() == 0

            data_to_send = 10

            for idx in range(data_to_send):
                data = {'counter': idx}
                packed = packer.pack(data)
                response = await tc.post(f"/hubs/{hub_name}/push", data=packed)
                assert response.status_code == 200

            response = await tc.get(f"/hubs/{hub_name}/history_size")
            assert response.status_code == 200
            assert response.json() == data_to_send

            response = await tc.get(f"/hubs/{hub_name}/buffer_size")
            assert response.status_code == 200
            assert response.json() == data_to_send

            response = await tc.get(f"/hubs")
            assert response.status_code == 200
            assert response.json() == [hub_name]

            last = await tc.get(f"/hubs/{hub_name}/last")
            assert last.status_code == 200
            unpacked = packer.unpack(last.content)
            assert unpacked == {'counter': data_to_send - 1}

            for idx in range(data_to_send):
                timeout = idx % 2
                pop = await tc.get(f"/hubs/{hub_name}/pop?timeout={timeout}")
                assert pop.status_code == 200
                unpacked = packer.unpack(pop.content)
                assert unpacked == {'counter': idx}

            pop = await tc.get(f"/hubs/{hub_name}/pop?timeout=0")
            assert pop.status_code == 204

            last_not_found = await tc.get(
                f"/hubs/{hub_name}/last?offset={data_to_send}"
            )
            assert last_not_found.status_code == 204

            response = await tc.get(f"/hubs/{hub_name}/history_size")
            assert response.status_code == 200
            assert response.json() == data_to_send

            response = await tc.get(f"/hubs/{hub_name}/buffer_size")
            assert response.status_code == 200
            assert response.json() == 0

            response = await tc.post(f"/hubs/{hub_name}/clear_history")
            assert response.status_code == 200

            response = await tc.post(f"/hubs/{hub_name}/clear_buffer")
            assert response.status_code == 200

            response = await tc.get(f"/hubs/{hub_name}/history_size")
            assert response.status_code == 200
            assert response.json() == 0

            response = await tc.get(f"/hubs/{hub_name}/buffer_size")
            assert response.status_code == 200
            assert response.json() == 0
