"""Formulate the driver template for backends.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

import os

import numpy as np
from schema import Or

from deposition import io
from deposition.drivers.molecular_dynamics_driver import MolecularDynamicsDriver
from deposition.enums import SettingsEnum


# FIXME: Template is inconsistent with implementation: Liskov Substitution Principle (LSP)
class TemplateDriver(MolecularDynamicsDriver):
    """Template to help with writing new MolecularDynamicsDriver classes."""

    schema_dict: dict = {
        "atomic_masses": list,
        "path_to_potential": os.path.exists,
        "thermostat_parameter": Or(float, int),
    }

    reserved_keywords = [
        "simulation_time",
    ]

    command = "${prefix} ${binary} ${arguments} < ${input_file} > ${output_file}"

    def __init__(self, driver_settings: dict, simulation_cell: dict) -> None:
        """Initialise template MD driver."""
        super().__init__(
            driver_settings,
            simulation_cell,
            command=self.command,
            schema_dict=self.schema_dict,
            reserved_keywords=self.reserved_keywords,
        )

    def write_inputs(
        self,
        filename: str,
        coordinates: np.ndarray,
        elements: list,
        velocities: np.ndarray,
        iteration_stage: str,
    ) -> None:
        """Write inputs to file."""
        def write_coordinates(file, coordinates: np.ndarray) -> None:
            pass

        def write_elements(file, elements: list) -> None:
            pass

        def write_velocities(file, velocities: np.ndarray) -> None:
            pass

        if iteration_stage == "deposition":
            simulation_time = self.settings[SettingsEnum.DEPOSITION_TIME.value]
        else:
            simulation_time = self.settings[SettingsEnum.RELAXATION_TIME.value]

        template_settings = self.settings.copy()
        template_settings.update({"simulation_time": simulation_time})
        io.write_file_using_template(
            f"{filename}.input",
            self.settings["path_to_input_template"],
            template_settings,
        )
        write_coordinates(f"{filename}.input", coordinates)
        write_elements(f"{filename}.input", elements)
        if iteration_stage == "deposition":
            write_velocities(f"{filename}.input", velocities)

    # FIXME: Implementations use State class but template doesn't.
    @staticmethod
    def read_outputs(filename: str) -> tuple[np.ndarray, list, np.ndarray]:
        """Read the outputs."""
        def read_coordinates(file) -> None:
            pass

        def read_elements(file) -> None:
            pass

        def read_velocities(file) -> None:
            pass

        coordinates = read_coordinates(f"{filename}.output")
        elements = read_elements(f"{filename}.output")
        velocities = read_velocities(f"{filename}.output")
        return coordinates, elements, velocities
