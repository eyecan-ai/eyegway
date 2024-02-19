__version__ = "0.0.1"
import loguru
import sys
import os

loguru.logger.remove()
loguru.logger.add(sys.stderr, level=os.environ.get("EYEGWAY_LOGGER_LEVEL", "INFO"))
