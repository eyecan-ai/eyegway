__version__ = "0.2.0"
import os
import sys

import loguru

loguru.logger.remove()
loguru.logger.add(sys.stderr, level=os.environ.get("EYEGWAY_LOGGER_LEVEL", "INFO"))
