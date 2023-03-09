"""Contains the specification of and maximum values of the algorithm
settings."""

from typeguard import typechecked

from neurondiscovery.grid_settings.Discovery import Discovery
from neurondiscovery.grid_settings.Explicit_ranges import DiscoveryRanges
from neurondiscovery.grid_settings.Specific_range import Specific_range
from neurondiscovery.neuron_types.Neuron_type import Neuron_type

# Initialise neuron parameter ranges
disco: Discovery = Discovery()
disco_ranges: Discovery = DiscoveryRanges()
specific_ranges: Discovery = Specific_range()


@typechecked
def get_selector_type(*, output_dir: str) -> Neuron_type:
    """Returns a neuron type that behaves as the redundant selector neurons;
    they start spiking at t=a_in_time+r, where r is the redundancy level in
    range [1,4]."""
    neuron_type = Neuron_type(
        a_in_time=10,
        grid_spec=disco_ranges,
        max_time=50,
        wait_after_input=1,
        name="selector",
        spike_input_type="one_spike",
        spike_output_type="continuous",
        output_dir=output_dir,
    )
    return neuron_type


@typechecked
def get_next_round_type(*, output_dir: str) -> Neuron_type:
    """Returns a neuron type that behaves as the redundant selector neurons;
    they spike once, at t=a_in_time+r, where r is the redundancy level in
    range.

    [1,4].
    """
    neuron_type = Neuron_type(
        a_in_time=6,
        grid_spec=disco_ranges,
        max_time=50,
        wait_after_input=1,
        name="next_round",
        spike_input_type="one_spike",
        spike_output_type="spike_once",
        output_dir=output_dir,
    )
    return neuron_type
