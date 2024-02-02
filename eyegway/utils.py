import loguru
import time


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
