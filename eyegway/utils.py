import loguru
import time
import datetime
import numpy as np
import cv2
import typing as t


class LoguruTimer:
    def __init__(self, name: str):
        self.name = name
        self.start = 0
        self.end = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        loguru.logger.debug(f"{self.name} took {self.end - self.start:.3f} seconds")


class DemoDataGenerator:

    def __init__(self) -> None:
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

        # Get the current time in local format
        current_text = text

        # Calculate the position to write the text in the middle
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(current_text, font, font_scale, font_thickness)[0]

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
            current_text,
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

        # Get the current time in local format
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    def generate(self) -> dict:
        data = {
            'image_0': self.generate_image_with_opencv(
                background_color=(0, 0, 0), foreground_color=(255, 255, 255)
            ),
            'image_1': self.generate_image_with_opencv(
                background_color=(255, 255, 255), foreground_color=(0, 0, 0)
            ),
            'image_2': self.generate_image_with_opencv(
                background_color=(74, 20, 140), foreground_color=(244, 255, 129)
            ),
            'image_counter_squared': self.generate_text_image_with_opencv(
                text=f"{self.counter}",
                size=(512, 512),
                background_color=(100, 100, 100),
                foreground_color=(255, 255, 255),
            ),
            'image_counter_letterbox': self.generate_text_image_with_opencv(
                text=f"{self.counter}",
                size=(512, 256),
                background_color=(100, 100, 100),
                foreground_color=(255, 255, 255),
            ),
            'image_counter_pillarbox': self.generate_text_image_with_opencv(
                text=f"{self.counter}",
                size=(256, 512),
                background_color=(100, 100, 100),
                foreground_color=(255, 255, 255),
            ),
            'metadata': {
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'author': 'Eyegway',
                'description': 'This is the demo data generator output',
                'counter': self.counter,
            },
            'counter': self.counter,
        }
        self.counter += 1
        return data
