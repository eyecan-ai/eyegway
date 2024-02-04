import eyegway.hubs.sync as ehs
import numpy as np
import time
import threading as th
import loguru

if __name__ == '__main__':

    hub_name = "test"  # make sure this hub is empty otherwise the example may not work
    tick_time = 0.3

    def receiver():
        hub = ehs.MessageHub.create(hub_name)

        while True:
            data = hub.pop()
            loguru.logger.info(f"Received data: {data['timestamp']}")
            if data["close"]:
                break

    def sender():
        hub = ehs.MessageHub.create(hub_name)
        hub.clear_buffer()
        hub.clear_history()

        max_iterations = 10
        for idx in range(10):
            data = {
                "timestamp": idx,
                "image": np.random.uniform(0, 255, (100, 100, 3)).astype(np.uint8),
                "close": idx == max_iterations - 1,
            }

            hub.push(data)
            loguru.logger.info(f"Sent data: {data['timestamp']}")
            time.sleep(tick_time)

    t0 = th.Thread(target=sender, daemon=True)
    t1 = th.Thread(target=receiver, daemon=True)
    t0.start(), t1.start(), t0.join(), t1.join()
