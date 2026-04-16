"""Defines driver Enum.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

from enum import Enum

import deposition


class DriverEnum(Enum):
    """Associate names with specific implemented driver classes."""

    LAMMPS = deposition.drivers.lammps_driver.LAMMPSDriver
    GULP = deposition.drivers.gulp_driver.GULPDriver
