import eyegway.hubs.asyn as eha
import numpy as np
import asyncio
import time
import threading as th
import loguru

if __name__ == '__main__':

    hub_name = "test"  # make sure this hub is empty otherwise the example may not work
    tick_time = 0.3

    async def receiver():
        hub = eha.AsyncMessageHub.create(hub_name)

        while True:
            data = await hub.pop()
            loguru.logger.info(f"Received data: {data['timestamp']}")
            if data["close"]:
                break

    async def sender():
        hub = eha.AsyncMessageHub.create(hub_name)
        await hub.clear_buffer()
        await hub.clear_history()

        max_iterations = 10
        for idx in range(10):
            data = {
                "timestamp": idx,
                "image": np.random.uniform(0, 255, (100, 100, 3)).astype(np.uint8),
                "close": idx == max_iterations - 1,
            }

            await hub.push(data)
            loguru.logger.info(f"Sent data: {data['timestamp']}")
            await asyncio.sleep(tick_time)

    t0 = th.Thread(target=lambda: asyncio.run(sender()), daemon=True)
    t1 = th.Thread(target=lambda: asyncio.run(receiver()), daemon=True)
    t0.start(), t1.start(), t0.join(), t1.join()
