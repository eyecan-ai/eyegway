import eyegway.hubs as eh
import numpy as np
import asyncio

if __name__ == '__main__':

    async def run():
        hub = eh.AsyncMessageHub.create("test")
        await hub.clear_buffer()
        await hub.clear_history()

        data = {
            "timestamp": 123456789,
            "image": {
                'a': {
                    'b': {
                        'c': np.random.uniform(0, 255, (100, 100, 3)).astype(np.uint8),
                    }
                }
            },
        }

        for _ in range(1):
            await hub.push(data)

        # retrieved_data = await hub.pop()
        # print("Timestamp:", retrieved_data["timestamp"])
        # print("Image shape:", retrieved_data["image"].shape)

    asyncio.run(run())
