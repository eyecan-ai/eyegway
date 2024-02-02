from redis.asyncio import Redis
from redis.asyncio.client import Pipeline
import eyegway.hubs as amc
import eyegway.communication as ecom
import eyegway.packaging as emp

if __name__ == "__main__":
    import asyncio
    import rich
    import fakeredis

    async def main():
        # cfg = HoctopussyConfig()
        # redis = Redis(host=cfg.host, port=cfg.port)
        redis = fakeredis.FakeAsyncRedis()
        channel = ecom.AsyncHistoryChannel(redis, "test")

        hub = amc.SimpleMessageHub(
            redis,
            "test",
            packer=emp.SmartMsgPacker(),
            max_buffer_size=5,
            max_history_size=5,
        )

        for idx in range(10):
            await hub.push(f"msg-{idx}")
        rich.print(await hub.last_multiple(0, 5))

    asyncio.run(main())
