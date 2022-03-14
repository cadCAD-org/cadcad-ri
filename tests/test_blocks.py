"""Testing blocks.

This should run as part of the CI/CD pipeline.
"""
from copy import copy as cp
from copy import deepcopy as dcp

import pytest
import numpy as np

from cadcad.spaces import Dimension, Space
from cadcad.trajectories import Point
from cadcad.dynamics import Block
from cadcad.errors import FreezingError, CopyError


def test_block_creation() -> None:
    """Test creation of blocks."""
