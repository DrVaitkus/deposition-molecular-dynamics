"""Defines custom types.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

from typing import TypeAlias

# Simple alias, path as used in the following functions uses a string rather
# than using the Python "Path" API, which takes a similar such string as argument.
path: TypeAlias = str
