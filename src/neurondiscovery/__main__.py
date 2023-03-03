"""Entry point for this project, runs the project code based on the cli command
that invokes this script."""

# Import code belonging to this project.


# mdsa = MDSA(list(range(0, 4, 1)))
# mdsa_configs = get_algo_configs(algo_spec=mdsa.__dict__)
# verify_algo_configs(algo_name="MDSA", algo_configs=mdsa_configs)

from src.neurondiscovery.discover import manage_simulation

# Parse command line interface arguments to determine what this script does.
# args = parse_cli_args()
from src.neurondiscovery.Discovery import Discovery
from src.neurondiscovery.Explicit_ranges import DiscoveryRanges
from src.neurondiscovery.Specific_range import Specific_range

disco = Discovery()
disco_ranges = DiscoveryRanges()
specific_ranges = Specific_range()

# Discovery_algo(disco=disco)
manage_simulation(disco=disco_ranges, max_time=100, a_in_time=5)
# Discovery_algo(disco=specific_ranges)
