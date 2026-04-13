"""Welcome to deposition.

Welcome to deposition, your favourite molecular dynamics
wrapper for deposition simulations written in Python.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

import importlib.metadata

from . import (
    drivers,
    enums,
    input_schema,
    io,
    physics,
    randomisation,
    settings,
    state,
    status,
    types,
    utils,
)
from .deposition import Deposition
from .iteration import Iteration
from .settings import Settings

# This takes the version from the package installation rather than manually.
__version__ = importlib.metadata.version("deposition")
