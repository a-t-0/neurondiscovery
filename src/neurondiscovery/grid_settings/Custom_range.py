"""Contains the specification of and maximum values of the algorithm
settings."""

from typing import List

from typeguard import typechecked

from neurondiscovery.grid_settings.Discovery import Discovery


# pylint: disable=R0902
# pylint: disable=R0903
# pylint: disable=R0913
class Custom_range(Discovery):
    """Specification of algorithm specification. Algorithm: Minimum Dominating
    Set Approximation by Alipour.

    Example usage: default_MDSA_alg=MDSA(some_vals=list(range(0, 4, 1)))
    """

    @typechecked
    def __init__(
        self,
        bias_range: List[float],
        du_range: List[float],
        dv_range: List[float],
        vth_range: List[float],
        weight_range: List[float],
        a_in_range: List[float],
        name: str,
    ) -> None:
        super().__init__()
        self.name = name

        # Specify supported values for du.
        # self.du_range = [-1, -0.5, -0.1, 0, 0.1, 0.5, 1]
        self.du_range = du_range

        # Specify supported values for dv.
        self.dv_range = dv_range

        # Specify supported values for u
        self.bias_range = bias_range

        # Specify supported values for u
        self.vth_range = vth_range

        # Specify supported values for weight
        self.weight_range = weight_range

        # Specify supported values for weight
        self.a_in_range = a_in_range
