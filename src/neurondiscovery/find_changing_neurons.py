"""Finds neurons that change over time, whilst still satisfying some pattern
(that may also change over time)."""
import copy
from typing import Dict, List, Union

from typeguard import typechecked

from src.neurondiscovery.discover import get_satisfactory_neurons
from src.neurondiscovery.Discovery import Discovery
from src.neurondiscovery.neuron_types.after_input.n_after_input_at_m import (
    n_after_input_at_m,
)
from src.neurondiscovery.print_behaviour import drawProgressBar
from src.neurondiscovery.Specific_range import Specific_range


@typechecked
def spike_one_timestep_later_per_property(
    a_in_time: int,
    neuron_dicts: List[Dict[str, Union[float, int, str]]],
    max_redundancy: int,
    wait_after_input: int,
) -> List[Dict[str, Union[int, float, str]]]:
    """Perform secondary loop on property increase/decreases per satisfactory.

    # neuron.
    """
    #
    count: int = 0
    explored_properties: List[str] = [
        "a_in",
        "a_in_time",
        "bias",
        "du",
        "dv",
        "vth",
        "weight",
    ]
    found_neurons: List[Dict[str, Union[int, float, str]]] = []
    for neuron_dict in neuron_dicts:
        for the_property in explored_properties:
            count += 1
            # specify disco.
            original_disco: Discovery = Specific_range()
            original_disco.du_range = [neuron_dict["du"]]
            original_disco.dv_range = [neuron_dict["dv"]]
            original_disco.bias_range = [neuron_dict["bias"]]
            original_disco.vth_range = [neuron_dict["vth"]]
            original_disco.weight_range = [neuron_dict["weight"]]
            original_disco.a_in_range = [int(neuron_dict["a_in"])]
            if count / (len(neuron_dicts) * len(explored_properties)) > 0.5470:
                if changes_over_time_correctly(
                    a_in_time=a_in_time,
                    disco=copy.deepcopy(original_disco),
                    max_redundancy=max_redundancy,
                    the_property=the_property,
                    wait_after_input=copy.deepcopy(wait_after_input),
                ):
                    found_neurons.append(neuron_dict)
                    found_neurons[-1]["property"] = the_property
                drawProgressBar(
                    percent=count
                    / (len(neuron_dicts) * len(explored_properties)),
                    barLen=100,
                    n_found=len(found_neurons),
                )
    return found_neurons


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
    for red_level in range(1, max_redundancy + 1):
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
            verbose=False,
            min_nr_of_neurons=10,
        )

        # if not empty list, proceed.
        if len(neuron_dicts) == 0:
            return False
        if red_level == max_redundancy:
            print(f"Changing: {the_property}, red_level{red_level}")
            return True
    return False


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


@typechecked
def print_changing_neuron(
    a_in_time: int,
    neuron_dict: Dict[str, Union[float, int, str]],
    the_property: str,
    max_redundancy: int,
    wait_after_input: int,
) -> None:
    """Perform secondary loop on property increase/decreases per satisfactory.

    # neuron.
    """
    lines: List = []

    # specify disco.
    disco: Discovery = Specific_range()
    disco.du_range = [neuron_dict["du"]]
    disco.dv_range = [neuron_dict["dv"]]
    disco.bias_range = [neuron_dict["bias"]]
    disco.vth_range = [neuron_dict["vth"]]
    disco.weight_range = [neuron_dict["weight"]]
    disco.a_in_range = [int(neuron_dict["a_in"])]

    # Simulate the neuron for n timesteps. Print
    print("The discovery ranges for redundancy respectively are:")
    for red_level in range(1, max_redundancy + 1):
        # Update discovery object.
        update_neuron_property(disco=disco, the_property=the_property)
        print(disco.__dict__)

        # Update wait_after_input.
        wait_after_input = wait_after_input + 1

        # specify spike pattern.
        expected_spikes: List[bool] = n_after_input_at_m(
            a_in_time=a_in_time,
            max_time=50,
            wait_after_input=wait_after_input,
        )

        if len(lines) != len(expected_spikes):
            for t in range(0, len(expected_spikes)):
                lines.append(str(t))
        for t, spikes in enumerate(expected_spikes):
            lines[t] = lines[t] + f"{red_level}:{spikes} | "
    print("")
    print("[t], [redundancy level]: spikes |")
    for line in lines:
        print(line)
