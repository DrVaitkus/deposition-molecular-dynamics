"""Runs the deposition from command line.

Copyright © 2021-2026 Martin J. Cyster. All Rights Reserved.
License details given in distributed LICENSE file.
"""

import sys

import click

import deposition
from deposition.settings import Settings
from deposition.types import path


@click.command()
@click.option("--settings", "settings_filename", required=True, type=click.Path(exists=True))
def main(settings_filename: path) -> None:
    """Run the deposition calculation from the command line.

    Usage: python3 run_deposition.py --settings SETTINGS_FILENAME

    Arguments:
        settings_filename (path): path to a YAML file containing settings for the simulation

    Returns:
        exit_code (int): a code relating to the reason for the termination of the calculation
    """
    settings = Settings.from_file(settings_filename).as_dict()
    calculation = deposition.Deposition(settings)
    return calculation.run()


if __name__ == "__main__":
    sys.exit(main())
