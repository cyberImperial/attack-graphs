from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulation.simulation import Simulation
