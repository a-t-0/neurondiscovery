"""Entry point for this project, runs the project code based on the cli command
that invokes this script."""

# Import code belonging to this project.


# mdsa = MDSA(list(range(0, 4, 1)))
# mdsa_configs = get_algo_configs(algo_spec=mdsa.__dict__)
# verify_algo_configs(algo_name="MDSA", algo_configs=mdsa_configs)

from typing import Dict, List, Union

# Parse command line interface arguments to determine what this script does.
# args = parse_cli_args()
from neurondiscovery.neuron_types.Neuron_type import Neuron_type
from neurondiscovery.neuron_types.sought_types import get_next_round_type
from neurondiscovery.search.manage_search import (
    find_changing_neurons,
    find_non_changing_neurons,
)

output_dir: str = "found_neurons"

# neuron_type:Neuron_type=get_selector_type(output_dir=output_dir)
neuron_type: Neuron_type = get_next_round_type(output_dir=output_dir)


static_neurons: List[Dict[str, Union[float, int]]] = find_non_changing_neurons(
    neuron_type=neuron_type, overwrite=True, verbose=True
)
found_neurons: List[Dict[str, Union[int, float, str]]] = find_changing_neurons(
    max_redundancy=4,
    neuron_type=neuron_type,
    print_verified_neurons=True,
    static_neurons=static_neurons,
    verify_shift=True,
    verbose=False,
)
