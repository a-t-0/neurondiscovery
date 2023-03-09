"""Contains the specification of and maximum values of the algorithm
settings."""
from typing import List

from typeguard import typechecked

from neurondiscovery.grid_settings.Discovery import Discovery
from neurondiscovery.import_export import create_output_dir_if_not_exists
from neurondiscovery.spike_patterns.expected_patterns import (
    n_after_input_at_m,
    one_after_input_at_a_in_time,
)
from neurondiscovery.spike_patterns.input_patterns import (
    get_single_input_spike,
)


# pylint: disable=R0902
# pylint: disable=R0903
class Neuron_type:
    """Stores different neuron types that can be searched."""

    # pylint: disable=R0913
    @typechecked
    def __init__(
        self,
        a_in_time: int,
        grid_spec: Discovery,
        max_time: int,
        name: str,
        spike_input_type: str,
        spike_output_type: str,
        output_dir: str,
        wait_after_input: int,
    ) -> None:
        # Specify filenames
        self.name: str = name
        self.type_dir: str = f"{output_dir}/{name}"

        # Store parameters
        self.a_in_time: int = a_in_time
        self.max_time: int = max_time
        self.wait_after_input: int = wait_after_input
        self.grid_spec: Discovery = grid_spec
        self.spike_input_type: str = spike_input_type
        self.spike_output_type: str = spike_output_type
        self.output_dir: str = output_dir

        # Get spike patterns.
        self.input_spikes: List[bool]
        if spike_input_type == "no_input":
            self.input_spikes = []
        elif spike_input_type == "one_spike":
            self.input_spikes = get_single_input_spike(
                a_in_time=self.a_in_time
            )
        elif spike_input_type == "n_continuous_spikes":
            raise NotImplementedError(
                f"Error, spike_input_type={spike_input_type} not yet "
                + "supported."
            )
        else:
            raise NotImplementedError(
                f"Error, spike_input_type={spike_input_type} not yet "
                + "supported."
            )

        self.expected_spikes = get_output_spike_pattern(
            a_in_time=self.a_in_time,
            max_time=self.max_time,
            wait_after_input=self.wait_after_input,
            spike_output_type=spike_output_type,
        )

        # TODO: allow for customisation.
        expected_spikes_without_input = [False] * max_time

        if len(self.input_spikes) > 0:
            if expected_spikes_without_input is None:
                raise ValueError(
                    "Error, expected_spikes_without_input is None."
                )
            assert expected_spikes_without_input is not None  # nosec
            self.expected_spikes_without_input: List[
                bool
            ] = expected_spikes_without_input

        create_output_dir_if_not_exists(output_dir)
        create_output_dir_if_not_exists(self.type_dir)


@typechecked
def get_output_spike_pattern(
    *,
    a_in_time: int,
    max_time: int,
    wait_after_input: int,
    spike_output_type: str,
) -> List[bool]:
    """Returns the expected spike pattern based on the neuron type."""
    expected_spikes: List[bool]
    if spike_output_type == "continuous":
        expected_spikes = n_after_input_at_m(
            a_in_time=a_in_time,
            max_time=max_time,
            wait_after_input=wait_after_input,
        )
    elif spike_output_type == "spike_once":
        expected_spikes = one_after_input_at_a_in_time(
            a_in_time=a_in_time,
            max_time=max_time,
            wait_after_input=wait_after_input,
        )
    else:
        raise NotImplementedError(
            f"Error, spike_output_type={spike_output_type} not yet "
            + "supported."
        )
    return expected_spikes
