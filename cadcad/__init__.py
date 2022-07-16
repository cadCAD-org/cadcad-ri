"""Initial configurations"""

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

logging.basicConfig(format="%(levelname)s: %(message)s")

__version__ = "0.1.0"
