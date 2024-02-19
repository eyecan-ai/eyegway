import eyegway.hubs as eh
import eyegway.hubs.sync as ehs
import numpy as np
import asyncio
import time
import threading as th
import loguru


if __name__ == '__main__':

    hub_name = "test_live_monitor"  # make sure this hub is empty otherwise the example may not work
    tick_time = 0.1
    history_size = 8

    def monitor():
        from rich.live import Live
        from rich.table import Table

        hub = ehs.MessageHub.create(hub_name)

        def generate_table():
            table = Table(title="Live Monitor")
            table.add_column("History Offset", style="cyan")
            table.add_column("Time", style="cyan")
            table.add_column("Counter", style="magenta")

            for off in range(history_size):
                data = hub.last(offset=off)
                if data is None:
                    table.add_row(str(off), "None", "None")
                else:
                    table.add_row(str(off), f'{data["time"]:.4f}', str(data["counter"]))

            return table

        with Live(generate_table(), refresh_per_second=10) as live:
            while True:
                live.update(generate_table())

    def producer():
        config = eh.HubsConfig()  # max_history_size=history_size)
        hub = ehs.MessageHub.create(hub_name, config=config)
        hub.clear_buffer()
        hub.clear_history()

        counter = 0
        while True:
            data = {"time": time.time(), "counter": counter}
            counter += 1

            hub.push(data)
            time.sleep(tick_time)

    t0 = th.Thread(target=producer, daemon=True)
    t1 = th.Thread(target=monitor, daemon=True)
    t0.start(), t1.start(), t0.join(), t1.join()
