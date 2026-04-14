"""Defines the Status class for tracking the status of simulations.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

from datetime import datetime as dt
from typing import TypeVar

import yaml

from deposition.enums import StatusEnum
from deposition.types import path

# This can be replaced with "Self" when we update to 3.11.
TStatus = TypeVar("TStatus", bound="Status")

class Status:
    """Track the status of the deposition calculation."""

    def __init__(
        self,
        iteration_number: int,
        sequential_failures: int,
        total_failures: int,
        pickle_location: path,
        last_updated: dt | None = None,
    ) -> None:
        """Initialise the status class."""
        if last_updated is None:
            self.last_updated = dt.now()
        else:
            self.last_updated = last_updated

        self.iteration_number = iteration_number
        self.sequential_failures = sequential_failures
        self.total_failures = total_failures
        self.pickle_location = pickle_location

    def write(self, filename: path) -> None:
        """Writes status information to `status.yaml`.

        Writes the current time, current iteration number, number of sequential
        failures, and the most recent saved state of the deposition simulation to
        `status.yaml`.
        """
        self.last_updated = dt.now()
        with open(filename, "w") as file:
            yaml.dump(self.as_dict(), file)

    @classmethod
    def from_file(cls, filename: path) -> TStatus:
        """Reads the status from the given file and return Status class."""
        try:
            with open(filename) as file:
                status = yaml.safe_load(file)
            return cls(
                int(status[StatusEnum.ITERATION_NUMBER.value]),
                int(status[StatusEnum.SEQUENTIAL_FAILURES.value]),
                int(status[StatusEnum.TOTAL_FAILURES.value]),
                str(status[StatusEnum.PICKLE_LOCATION.value]),
                status[StatusEnum.LAST_UPDATED.value],
            )
        except FileNotFoundError as bad_file:
            raise FileNotFoundError(f"status file not found: {filename}") from bad_file

    def as_dict(self) -> dict:
        """Returns the status as a dictionary."""
        return {
            StatusEnum.ITERATION_NUMBER.value: self.iteration_number,
            StatusEnum.SEQUENTIAL_FAILURES.value: self.sequential_failures,
            StatusEnum.TOTAL_FAILURES.value: self.total_failures,
            StatusEnum.PICKLE_LOCATION.value: self.pickle_location,
            StatusEnum.LAST_UPDATED.value: self.last_updated,
        }
