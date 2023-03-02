"""Contains the specification of and maximum values of the algorithm
settings."""
from typing import List, Optional, Union

from typeguard import typechecked


# pylint: disable=R0902
# pylint: disable=R0903
class Discovery:
    """Specification of algorithm specification. Algorithm: Minimum Dominating
    Set Approximation by Alipour.

    Example usage: default_MDSA_alg=MDSA(some_vals=list(range(0, 4, 1)))
    """

    @typechecked
    def __init__(
        self,
    ) -> None:
        self.name = "Discovery"

        # Specify supported values for du.
        du_min: float = -1
        du_max: float = 1
        du_len: int = 10
        self.du_range = self.get_range(
            min_val=du_min,
            max_val=du_max,
            length=du_len,
        )

        # Specify svpported valves for dv.
        dv_min: float = -1
        dv_max: float = 1
        dv_len: int = 10
        self.dv_range = self.get_range(
            min_val=dv_min,
            max_val=dv_max,
            length=dv_len,
        )

        # Specify supported biasalbiases for bias
        bias_min: float = 0
        bias_max: float = 10
        bias_len: int = 10
        self.bias_range = self.get_range(
            min_val=bias_min,
            max_val=bias_max,
            length=bias_len,
        )

        # Specify supported vthalvthes for vth
        vth_min: float = 0
        vth_max: float = 10
        vth_len: int = 10
        self.vth_range = self.get_range(
            min_val=vth_min,
            max_val=vth_max,
            length=vth_len,
        )

        # Specify supported vthalvthes for vth
        weight_min: int = -10
        weight_max: int = 10
        self.weight_range = self.get_range(
            min_val=weight_min,
            max_val=weight_max,
        )
        self.a_in_range = list(range(1, 10))
        self.a_in_time = 4

    @typechecked
    def get_range(
        self,
        min_val: Union[float, int],
        max_val: Union[float, int],
        length: Optional[int] = None,
    ) -> List[Union[float, int]]:
        """Returns a list with the values in a range."""
        if length is not None:
            return [
                min_val + i * (max_val - min_val) / length
                for i in range(length)
            ]
        if not isinstance(min_val, int) or not isinstance(min_val, int):
            raise TypeError(
                "Error, min or max value without length specification "
                + f"requires integers. Found min:{min_val},max:{max_val}"
            )
        return list(range(int(min_val), int(max_val)))
