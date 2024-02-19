# Table of Contents

- [Hubs Producer / Consumer](#hubs-producer--consumer)
- [Hubs Monitor](#hubs-monitor)

## Hubs Producer / Consumer

In this example, we will show how to use the `hubs` module to create a simple producer and consumer
scenario. The producer will send data to a hub, and the consumer will `pop` data from the hub.
Popping data from the hub will remove the data from the hub's queue.
In the examples the producer sends a timestamp an image and a close _Flag_ to the hub, and the consumer pulls the data from the hub and prints the timestamp and the image. The close _Flag_ is used to stop the
consumer.

To launch the Async version of the producer and consumer, run the following commands:

```console
python producer_consumer_async.py
```

To launch the Sync version of the producer and consumer, run the following commands:

```console
python producer_consumer_sync.py
```

## Hubs Monitor

In this example we will show how to use the `hubs` module to create a simple monitor. The monitor will
`get` the data from the hub and print it. The difference between the monitor and the consumer is
that the monitor will not remove the data from the hub but just read it from the data history. The
history can be queried for a specific offset: **0** means the last data, **1** the second last and so on.

To launch the monitor, run the following command:

```console
python live_monitor.py
```

In this example we will show also how to override default settings for the hub. The hub will be created
with a custom configuration to resize the history max size.
