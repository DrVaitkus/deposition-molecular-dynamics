"""Defines the functions for post-processing simulations.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

from enum import Enum

import numpy as np

from deposition.state import State
from deposition.utils import generate_neighbour_list, get_simulation_cell, unwrap_z_coordinates


# FIXME: Positional bool with default
def run(name: str, state: State, simulation_cell: dict, parameters=None, dry_run=False) -> None:
    """Runs the postprocessing check on the provided structural data.

    Args:
        name (str): the string referring to the check
        state (State): coordinates, elements, velocities
        simulation_cell (dict): size and shape of the simulation cell
        parameters: any arguments required for the check
        dry_run: optionally skip the actual check (for validation at initialisation)
    """
    try:
        postprocessing_class = PostProcessingEnum[name].value
        routine = postprocessing_class(state, simulation_cell, parameters)
    except KeyError as bad_routine:
        raise ValueError(f"unknown post processing routine {name}") from bad_routine

    if not dry_run:
        return routine.run()
    return None


class NumNeighboursCheck:
    """Class for checking the number of neighbours.

    Assess the number of neighbours of all simulated atoms to check that
    everything is bonded together and there are no isolated regions.

    Parameters:
        - min_neighbours (`int`)
            - the minimum number of neighbouring atoms for each atom
        - bonding distance cutoff (Angstroms, `int` or `float`)
            - minimum separation for two atoms to be considered bonded
    """

    num_parameters = 2
    default_parameters = (1, 4.0)

    def __init__(self, state: State, simulation_cell: dict, parameters) -> None:
        """Initialise the number of neighbours check."""
        if parameters is None:
            parameters = self.default_parameters

        if len(parameters) != self.num_parameters:
            raise ValueError(f"{self.__class__} requires {self.num_parameters} argument(s)")

        self.min_neighbours = float(parameters[0])
        self.bonding_cutoff = float(parameters[1])
        self.state = state
        self.simulation_cell = simulation_cell

    def run(self) -> State:
        """Check the number of neighbours."""
        neighbour_list = generate_neighbour_list(
            self.simulation_cell, self.state.coordinates, self.bonding_cutoff
        )
        if np.any(np.less_equal(neighbour_list, self.min_neighbours)):
            raise RuntimeWarning("one or more atoms has too few neighbouring atoms")
        return self.state



class ShiftToOrigin:
    """Relocates the entire atomic structure to the origin (0,0,0) at the end of each iteration."""

    default_parameters = False

    #FIXME: The input parameter is unused, this just automatically applies the default.
    def __init__(self, state: State, simulation_cell: dict, *args: bool) -> None:
        """Initialise the shift to origin class."""
        if args is None:
            args = self.default_parameters
        if not isinstance(args[0], bool):
            raise TypeError("shift to origin routine must be True or False")
        self.state = state
        self.simulation_cell = simulation_cell
        self.perform_shift = args[0]

    def run(self) -> State:
        """Moves the bottom of the atoms back to z=0 and leaves remaining atoms unchanged."""
        full_simulation_cell = get_simulation_cell(self.simulation_cell)

        if self.perform_shift:
            new_coordinates = unwrap_z_coordinates(full_simulation_cell, self.state.coordinates)
            minimum_z = np.min(new_coordinates[:, 2])
            new_coordinates[:,2] -= minimum_z
        else:
            new_coordinates = self.state.coordinates.__copy__()

        return State(new_coordinates, self.state.elements, self.state.velocities)


class PostProcessingEnum(Enum):
    """Map strings to postprocessing routines."""

    num_neighbours = NumNeighboursCheck
    shift_to_origin = ShiftToOrigin
