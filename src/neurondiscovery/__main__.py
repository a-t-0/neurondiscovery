"""Entry point for this project, runs the project code based on the cli command
that invokes this script."""

# Import code belonging to this project.


# mdsa = MDSA(list(range(0, 4, 1)))
# mdsa_configs = get_algo_configs(algo_spec=mdsa.__dict__)
# verify_algo_configs(algo_name="MDSA", algo_configs=mdsa_configs)

import os
from typing import Dict, List, Union

from src.neurondiscovery.discover import get_satisfactory_neurons

# Parse command line interface arguments to determine what this script does.
# args = parse_cli_args()
from src.neurondiscovery.Discovery import Discovery
from src.neurondiscovery.Explicit_ranges import DiscoveryRanges
from src.neurondiscovery.find_changing_neurons import (
    spike_one_timestep_later_per_property,
)
from src.neurondiscovery.import_export import (
    load_dict_from_file,
    write_dict_to_file,
)
from src.neurondiscovery.neuron_types.after_input.n_after_input_at_m import (
    n_after_input_at_m,
)
from src.neurondiscovery.Specific_range import Specific_range

# Initialise neuron parameter ranges
disco: Discovery = Discovery()
disco_ranges: Discovery = DiscoveryRanges()
specific_ranges: Discovery = Specific_range()
neuron_dicts: List[Dict[str, Union[float, int]]] = []
filepath: str = "example.json"

# Get expected spike pattern.
a_in_time: int = 10
wait_after_input = 4

expected_spikes: List[bool] = n_after_input_at_m(
    a_in_time=a_in_time,
    max_time=50,
    wait_after_input=wait_after_input,
)

# If neuron properties already exist, load from file.
if os.path.isfile(filepath):
    neuron_dicts = load_dict_from_file(filepath)
else:
    neuron_dicts = get_satisfactory_neurons(
        a_in_time=a_in_time,
        disco=disco_ranges,
        expected_spikes=expected_spikes,
        max_neuron_props={"vth": 100},
        min_neuron_props={"vth": -100},
        min_nr_of_neurons=10,
    )

    # Write neuron properties to file.
    write_dict_to_file(filepath="example.json", neuron_dicts=neuron_dicts)

print("neuron_dicts")
print(neuron_dicts)

max_redundancy: int = 10
spike_one_timestep_later_per_property(
    a_in_time=a_in_time,
    neuron_dicts=neuron_dicts,
    max_redundancy=max_redundancy,
    wait_after_input=wait_after_input,
)
