"""Defines the State class for tracking coords, atoms and velocities of simulations.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

import logging
import pickle
from typing import TypeVar

import numpy as np

from deposition.enums import StateEnum
from deposition.types import path

# This can be replaced with "Self" when we update to 3.11.
TState = TypeVar("TState", bound="State")


class State:
    """Store coordinates, elements, and velocities for a set of atoms."""

    def __init__(self, coordinates: np.ndarray, elements: list, velocities: np.ndarray) -> None:
        """Initialises state object with coords, elements and velocities."""
        self.coordinates: np.ndarray = coordinates
        self.elements: list = elements
        self.velocities: np.ndarray = velocities

    def write(
        self, pickle_location: path, include_velocities: bool = True  # FIXME: default bool
    ) -> None:
        """Write current state to a pickle file.

        Arguments:
            pickle_location (path): path to save the pickled data to
            include_velocities (bool): whether to save velocities or not
        """
        data = {
            StateEnum.COORDINATES.value: self.coordinates,
            StateEnum.ELEMENTS.value: self.elements,
            StateEnum.VELOCITIES.value: self.velocities if include_velocities else None,
        }
        logging.info(f"writing state to {pickle_location}")
        with open(pickle_location, "wb") as file:
            pickle.dump(data, file)

    @classmethod
    def read_state(cls, pickle_location: path) -> TState:
        """Reads current state of calculation from pickle file.

        The pickle file stores the state, species (elements),
        and velocities of all simulated atoms.

        Arguments:
            pickle_location (path): path read the pickled data from

        Returns:
            state: state, elements, velocities
        """
        logging.info(f"reading state from {pickle_location}")
        with open(pickle_location, "rb") as file:
            data = pickle.load(file)  # FIXME: security risk
        return cls(
            data[StateEnum.COORDINATES.value],
            data[StateEnum.ELEMENTS.value],
            data[StateEnum.VELOCITIES.value],
        )
