"""Finds neurons that change over time, whilst still satisfying some pattern
(that may also change over time)."""
import copy
import sys
from typing import Dict, List, Union

from typeguard import typechecked

from src.neurondiscovery.discover import get_satisfactory_neurons
from src.neurondiscovery.Discovery import Discovery
from src.neurondiscovery.neuron_types.after_input.n_after_input_at_m import (
    n_after_input_at_m,
)
from src.neurondiscovery.Specific_range import Specific_range


@typechecked
def spike_one_timestep_later_per_property(
    a_in_time: int,
    neuron_dicts: List[Dict[str, Union[float, int]]],
    max_redundancy: int,
    wait_after_input: int,
) -> None:
    """Perform secondary loop on property increase/decreases per satisfactory.

    # neuron.
    """
    #
    for neuron_dict in neuron_dicts:
        for the_property in [
            "a_in",
            "a_in_time",
            "bias",
            "du",
            "dv",
            "vth",
            "weight",
        ]:
            # specify disco.
            original_disco: Discovery = Specific_range()
            original_disco.du_range = [neuron_dict["du"]]
            original_disco.dv_range = [neuron_dict["dv"]]
            original_disco.bias_range = [neuron_dict["bias"]]
            original_disco.vth_range = [neuron_dict["vth"]]
            original_disco.weight_range = [neuron_dict["weight"]]
            original_disco.a_in_range = [int(neuron_dict["a_in"])]
            if changes_over_time_correctly(
                a_in_time=a_in_time,
                disco=copy.deepcopy(original_disco),
                max_redundancy=max_redundancy,
                the_property=the_property,
                wait_after_input=copy.deepcopy(wait_after_input),
            ):
                print(f"Found for:{the_property} at:")
                print(neuron_dict)
                sys.exit()


@typechecked
def changes_over_time_correctly(
    a_in_time: int,
    disco: Discovery,
    max_redundancy: int,
    the_property: str,
    wait_after_input: int,
) -> bool:
    """Perform secondary loop on property increase/decreases per satisfactory.

    # neuron.
    """
    for _ in range(1, max_redundancy + 1):
        # Update discovery object.
        update_neuron_property(disco=disco, the_property=the_property)

        # Update wait_after_input.
        wait_after_input = wait_after_input + 1

        # specify spike pattern.
        expected_spikes: List[bool] = n_after_input_at_m(
            a_in_time=a_in_time,
            max_time=50,
            wait_after_input=wait_after_input,
        )

        # simulate snn.
        neuron_dicts = get_satisfactory_neurons(
            a_in_time=a_in_time,
            disco=disco,
            expected_spikes=expected_spikes,
            max_neuron_props={"vth": 100},
            min_neuron_props={"vth": -100},
            min_nr_of_neurons=10,
        )

        # if not empty list, proceed.
        if len(neuron_dicts) == []:
            return False
    return True


@typechecked
def update_neuron_property(disco: Discovery, the_property: str) -> None:
    """adds red_level to a certain neuron the_property."""
    if the_property == "a_in":
        disco.a_in_range = [disco.a_in_range[0] + 1]
    if the_property == "bias":
        disco.bias_range = [disco.bias_range[0] + 1]
    if the_property == "du":
        disco.du_range = [disco.du_range[0] + 1]
    if the_property == "dv":
        disco.dv_range = [disco.dv_range[0] + 1]
    if the_property == "vth":
        disco.vth_range = [disco.vth_range[0] + 1]
    if the_property == "weight":
        disco.weight_range = [disco.weight_range[0] + 1]
