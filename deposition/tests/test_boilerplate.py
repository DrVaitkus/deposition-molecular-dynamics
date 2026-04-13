"""Testing whether we can even import deposition.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

import deposition


def test_boilerplate_name() -> None:
    """Test that we can import deposition and resolve its name."""
    deposition.__name__


def test_boilerplate_version() -> None:
    """Test that we can import deposition and resolve its version number."""
    deposition.__version__
