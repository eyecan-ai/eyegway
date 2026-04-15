import asyncio
import datetime
import inspect
import math
import random
import time
import typing as t
from abc import ABC, abstractmethod

import cv2
import numpy as np
from rich import print

from eyegway.hubs.asyn import AsyncMessageHub
from eyegway.hubs.sync import MessageHub

start_time = time.time()


class DataGenerator(ABC):
    """
    Base class for data generators.
    Generates data and pushes it to a message hub at regular intervals.
    Supports both synchronous and asynchronous message hubs.
    """

    @abstractmethod
    def generate(self) -> dict[str, t.Any]:
        """
        Generate data to be pushed to the hub.

        Returns:
            dict[str, Any]: The generated data.
        """
        pass


class DataPusher:
    def __init__(
        self,
        generator: DataGenerator,
        target_hub: MessageHub | AsyncMessageHub,
        interval: float = 0.1,
    ) -> None:
        """
        Initialize the data generator.

        Args:
            hub (MessageHub | AsyncMessageHub): The message hub to push data to.
            interval (float): The time interval between data generations.
        """
        self.hub = target_hub
        self.generator = generator
        self.interval = interval
        self.is_async = inspect.iscoroutinefunction(target_hub.push)

    async def run_async(self) -> None:
        """
        Start the asynchronous data generation loop.
        """
        try:
            while True:
                data = self.generator.generate()
                await self.hub.push(data)  # type: ignore
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            print(f"Stopped data generation for {self.hub.name}")

    def run_sync(self) -> None:
        """
        Start the synchronous data generation loop.
        """
        try:
            while True:
                data = self.generator.generate()
                self.hub.push(data)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print(f"Stopped data generation for {self.hub.name}")


class RandomWalkGenerator(DataGenerator):
    """
    Data generator for simulating a random walk.
    """

    def __init__(self) -> None:
        super().__init__()
        self.current_value: float = 0.0

    def generate(self) -> dict[str, t.Any]:
        """
        Generate the next value in the random walk.

        Returns:
            dict[str, Any]: The generated data point.
        """
        self.current_value += random.uniform(-1, 1)  # noqa: S311
        return {
            "time": time.time() - start_time,
            "value": self.current_value,
        }


class SineGenerator(DataGenerator):
    """
    Data generator for simulating a sine wave.
    """

    def __init__(
        self,
        interval: float = 0.1,
    ) -> None:
        super().__init__()
        self.interval = interval
        self.time_step: float = 0.0

    def generate(self) -> dict[str, t.Any]:
        """
        Generate the next value in the sine wave.

        Returns:
            dict[str, Any]: The generated data point.
        """
        self.time_step += self.interval
        value = math.sin(self.time_step)
        return {"time": time.time() - start_time, "value": value}


class HelixGenerator(DataGenerator):
    """
    Data generator for simulating a helix.
    """

    def __init__(self, interval: float = 0.1) -> None:
        super().__init__()
        self.interval = interval
        self.time_step: float = 0.0

    def generate(self) -> dict[str, t.Any]:
        """
        Generate the next value in the helix.

        Returns:
            dict[str, Any]: The generated data point.
        """
        self.time_step += self.interval
        value_y = math.sin(self.time_step)
        value_z = math.cos(self.time_step)
        return {"time": time.time() - start_time, "value": value_y, "height": value_z}


class DailyProductionGenerator(DataGenerator):
    """
    Data generator for simulating daily production data.
    """

    def __init__(
        self,
        interval: float = 0.1,
        min_value: int = 80,
        max_value: int = 120,
    ) -> None:
        super().__init__()
        self.interval = interval
        self.min_value = min_value
        self.max_value = max_value

    def generate(self) -> dict[str, t.Any]:
        """
        Generate a random production value.

        Returns:
            dict[str, Any]: The generated data point.
        """
        value = random.uniform(self.min_value, self.max_value)  # noqa: S311
        return {"time": time.time() - start_time, "value": value}


class DemoDataGenerator(DataGenerator):
    """
    Data generator for generating demo images with OpenCV.
    Supports both synchronous and asynchronous message hubs.
    """

    def __init__(self) -> None:
        super().__init__()
        self.counter = 0

    def generate_text_image_with_opencv(
        self,
        text: str,
        size: t.Sequence = (512, 512),
        background_color: t.Sequence = (0, 0, 0),
        foreground_color: t.Sequence = (255, 255, 255),
        font_scale: int = 4,
        font_thickness: int = 4,
    ) -> np.ndarray:
        """
        Generate an image with text using OpenCV.

        Args:
            text (str): The text to display on the image.
            size (Sequence): The size of the image.
            background_color (Sequence): The background color of the image.
            foreground_color (Sequence): The color of the text.
            font_scale (int): The scale of the font.
            font_thickness (int): The thickness of the font.

        Returns:
            np.ndarray: The generated image.
        """
        # Calculate the position to write the text in the middle
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

        width = int(text_size[0] * 1.2)
        height = width

        # Create background image
        image = np.ones((height, width, 3), dtype=np.uint8)
        image[:, :] = background_color

        # Draw the text in the middle of the image
        x = (width - text_size[0]) // 2
        y = (height + text_size[1]) // 2
        cv2.putText(
            image,
            text,
            (x, y),
            font,
            font_scale,
            foreground_color,
            font_thickness,
        )

        # Resize
        image = cv2.resize(image, size)
        return image

    def generate_image_with_opencv(
        self,
        size: t.Sequence = (512, 512),
        background_color: t.Sequence = (0, 0, 0),
        foreground_color: t.Sequence = (255, 255, 255),
        font_scale: int = 4,
        font_thickness: int = 4,
    ) -> np.ndarray:
        """
        Generate an image with the current time using OpenCV.

        Args:
            size (Sequence): The size of the image.
            background_color (Sequence): The background color of the image.
            foreground_color (Sequence): The color of the text.
            font_scale (int): The scale of the font.
            font_thickness (int): The thickness of the font.

        Returns:
            np.ndarray: The generated image.
        """
        # Get the current time in local format
        current_time = datetime.datetime.now().strftime(  #  noqa: DTZ005
            "%Y-%m-%d %H:%M:%S"
        )

        # Calculate the position to write the text in the middle
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(current_time, font, font_scale, font_thickness)[0]

        width = int(text_size[0] * 1.2)
        height = width

        # Create background image
        image = np.ones((height, width, 3), dtype=np.uint8)
        image[:, :] = background_color

        # Draw the current time in the middle of the image
        x = (width - text_size[0]) // 2
        y = (height + text_size[1]) // 2
        cv2.putText(
            image,
            current_time,
            (x, y),
            font,
            font_scale,
            foreground_color,
            font_thickness,
        )

        # Resize
        image = cv2.resize(image, size)
        return image

    def generate(self) -> dict[str, t.Any]:
        """
        Generate demo data.

        Returns:
            dict[str, Any]: The generated data.
        """
        data = {
            "image_0": self.generate_image_with_opencv(
                background_color=(0, 0, 0), foreground_color=(255, 255, 255)
            ),
            "image_1": self.generate_image_with_opencv(
                background_color=(255, 255, 255), foreground_color=(0, 0, 0)
            ),
            "image_2": self.generate_image_with_opencv(
                background_color=(74, 20, 140), foreground_color=(244, 255, 129)
            ),
            "image_counter_squared": self.generate_text_image_with_opencv(
                text=f"{self.counter}",
                size=(512, 512),
                background_color=(100, 100, 100),
                foreground_color=(255, 255, 255),
            ),
            "image_counter_letterbox": self.generate_text_image_with_opencv(
                text=f"{self.counter}",
                size=(512, 256),
                background_color=(100, 100, 100),
                foreground_color=(255, 255, 255),
            ),
            "image_counter_pillarbox": self.generate_text_image_with_opencv(
                text=f"{self.counter}",
                size=(256, 512),
                background_color=(100, 100, 100),
                foreground_color=(255, 255, 255),
            ),
            "metadata": {
                "timestamp": datetime.datetime.now().strftime(  # noqa: DTZ005
                    "%Y-%m-%d %H:%M:%S"
                ),
                "author": "Eyegway",
                "description": "This is the demo data generator output",
                "counter": self.counter,
            },
            "counter": self.counter,
        }
        self.counter += 1
        return data
