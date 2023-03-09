"""Entry point for this project, runs the project code based on the cli command
that invokes this script."""

# Import code belonging to this project.


# mdsa = MDSA(list(range(0, 4, 1)))
# mdsa_configs = get_algo_configs(algo_spec=mdsa.__dict__)
# verify_algo_configs(algo_name="MDSA", algo_configs=mdsa_configs)

from typing import Dict, List, Union

# Parse command line interface arguments to determine what this script does.
# args = parse_cli_args()
from neurondiscovery.grid_settings.Discovery import Discovery
from neurondiscovery.grid_settings.Explicit_ranges import DiscoveryRanges
from neurondiscovery.grid_settings.Specific_range import Specific_range
from neurondiscovery.neuron_types.Neuron_type import Neuron_type
from neurondiscovery.search.manage_search import (
    find_changing_neurons,
    find_non_changing_neurons,
)

output_dir: str = "found_neurons"

# Initialise neuron parameter ranges
disco: Discovery = Discovery()
disco_ranges: Discovery = DiscoveryRanges()
specific_ranges: Discovery = Specific_range()


neuron_type = Neuron_type(
    a_in_time=10,
    grid_spec=disco_ranges,
    max_time=50,
    wait_after_input=1,
    name="selector",
    spike_input_type="one_spike",
    output_dir=output_dir,
)

static_neurons: List[Dict[str, Union[float, int]]] = find_non_changing_neurons(
    neuron_type=neuron_type, overwrite=False
)
found_neurons: List[Dict[str, Union[int, float, str]]] = find_changing_neurons(
    max_redundancy=4,
    neuron_type=neuron_type,
    print_verified_neurons=True,
    static_neurons=static_neurons,
    verify_shift=True,
)
