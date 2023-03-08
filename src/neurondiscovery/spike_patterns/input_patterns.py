"""Returns some input spike train."""
from typing import List

from typeguard import typechecked


@typechecked
def get_single_input_spike(a_in_time: int) -> List[bool]:
    """Returns list with False, and one True at index time a_in_time+1."""
    spikes: List[bool] = [False] * a_in_time
    spikes.append(True)
    print(f"a_in_time={a_in_time}")
    print(f"spikes={spikes}")
    return spikes
