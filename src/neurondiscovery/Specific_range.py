"""Contains the specification of and maximum values of the algorithm
settings."""

from typeguard import typechecked

from src.neurondiscovery.Discovery import Discovery


# pylint: disable=R0902
# pylint: disable=R0903
class Specific_range(Discovery):
    """Specification of algorithm specification. Algorithm: Minimum Dominating
    Set Approximation by Alipour.

    Example usage: default_MDSA_alg=MDSA(some_vals=list(range(0, 4, 1)))
    """

    @typechecked
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.name = "Discovery"

        # Specify supported values for du.
        # self.du_range = [-1, -0.5, -0.1, 0, 0.1, 0.5, 1]
        self.du_range = [0.1]

        # Specify supported values for dv.
        self.dv_range = [-1.0]

        # Specify supported values for u
        self.bias_range = [0.0]

        # Specify supported values for u
        self.vth_range = [5.0]

        # Specify supported values for weight
        self.weight_range = [1]

        # Specify supported values for weight
        self.a_in_range = list(range(5, 6))
        self.a_in_time = 14
