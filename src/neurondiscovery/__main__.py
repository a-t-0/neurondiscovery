"""Entry point for this project, runs the project code based on the cli command
that invokes this script."""

# Import code belonging to this project.


# mdsa = MDSA(list(range(0, 4, 1)))
# mdsa_configs = get_algo_configs(algo_spec=mdsa.__dict__)
# verify_algo_configs(algo_name="MDSA", algo_configs=mdsa_configs)

from src.neurondiscovery.discover import discover_neuron_type

# Parse command line interface arguments to determine what this script does.
# args = parse_cli_args()
from src.neurondiscovery.Discovery import Discovery
from src.neurondiscovery.Explicit_ranges import DiscoveryRanges
from src.neurondiscovery.Specific_range import Specific_range

disco = Discovery()
disco_ranges = DiscoveryRanges()
specific_ranges = Specific_range()

# Discovery_algo(disco=disco)
discover_neuron_type(disco=disco_ranges)
# Discovery_algo(disco=specific_ranges)
