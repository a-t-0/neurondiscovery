"""Creates a spike pattern that starts firing n timesteps after a spike input
at time step m."""
# pylint: disable=R0913
from typing import List

from typeguard import typechecked


@typechecked
def n_after_input_at_m(
    a_in_time: int, max_time: int, wait_after_input: int
) -> List[bool]:
    """Creates a spike pattern that starts firing n timesteps after a spike
    input at time step m."""
    spike_train: List[bool] = []
    for t in range(0, max_time + 1):
        if t < (a_in_time + wait_after_input):
            spike_train.append(False)
        else:
            spike_train.append(True)
    return spike_train
