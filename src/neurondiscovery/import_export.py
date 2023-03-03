"""Imports and exports neuron property dictionaries."""
import json
import os
from typing import Dict, List, Union

from typeguard import typechecked


@typechecked
def write_dict_to_file(
    filepath: str, neuron_properties: List[Dict[str, Union[float, int]]]
) -> None:
    """Writes dict to json file."""
    # Serialize data into file:
    with open(filepath, "w", encoding="utf-8") as some_file:
        json.dump(neuron_properties, some_file)

    # Assert file exists.
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"Error, {filepath} was not found after exporting data."
        )

    # Assert data can be loaded from file.
    loaded_data: List[Dict[str, Union[float, int]]] = load_dict_from_file(
        filepath
    )

    # Assert loaded data equals input data.
    if loaded_data != neuron_properties:
        raise LookupError("Error, loaded data does not equal outputted data.")


@typechecked
def load_dict_from_file(filepath: str) -> List[Dict[str, Union[float, int]]]:
    """Loads json file into list of dicts."""

    # Assert file exists.
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"Error, {filepath} was not found after exporting data."
        )

    # Read data from file:
    with open(filepath, encoding="utf-8") as some_file:
        neuron_properties = json.load(some_file)
    return neuron_properties
