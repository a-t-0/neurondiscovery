"""Contains the specification of and maximum values of the algorithm
settings."""
from typing import List, Optional

from typeguard import typechecked


# pylint: disable=R0902
# pylint: disable=R0903
class Neuron_types:
    """Stores different neuron types that can be searched."""

    @typechecked
    def __init__(
        self,
        name: str,
        input_spikes: List[int],
        expected_spikes: List[bool],
        expected_spikes_without_input: Optional[List[bool]],
    ) -> None:
        self.name: str = name
        self.input_spikes: List[int] = input_spikes
        self.expected_spikes: List[bool] = expected_spikes
        if len(input_spikes) > 0:
            if expected_spikes_without_input is None:
                raise ValueError(
                    "Error, expected_spikes_without_input is None."
                )
            assert expected_spikes_without_input is not None  # nosec
            self.expected_spikes_without_input: List[
                bool
            ] = expected_spikes_without_input
