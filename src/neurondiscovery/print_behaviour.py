"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801


import sys
from typing import Dict, List, Optional, Union

import networkx as nx
from typeguard import typechecked


@typechecked
def manage_printing(
    *,
    expected_spikes: List[bool],
    neuron_dicts: List[Dict[str, Union[float, int]]],
    node_name: str,
    working_snns: List[nx.DiGraph],
    print_behaviour: Optional[bool] = None,
) -> None:
    """Prints relevant simulation data if desired.."""
    # Print found neuron results.
    print("")
    if len(working_snns) > 0:
        print("Found the following neurons that satisfy the requirements:")
    else:
        print(
            "Did not find neurons that satisfy the requirements."
            + f"{expected_spikes}"
        )

        print("")
    if print_behaviour:
        print_found_neuron_behaviour(
            node_name=node_name,
            snns=working_snns,
            t_max=min(len(expected_spikes), 50),
        )

    for neuron_property in neuron_dicts:
        print(neuron_property)


# pylint: disable=R0913
@typechecked
def print_found_neuron_behaviour(
    *, node_name: str, snns: List[nx.DiGraph], t_max: int
) -> None:
    """Prints: spikes, u, v for the first max_t timesteps."""
    for snn in snns:
        for t in range(0, t_max):
            neuron = snn.nodes[node_name]["nx_lif"][t]
            print(f"{t},{neuron.spikes},u={neuron.u.get()},v={neuron.v.get()}")


@typechecked
def get_node_name_neuron_dicts(
    *,
    a_in_time: int,
    input_node_name: str,
    node_name: str,
    snns: List[nx.DiGraph],
) -> List[Dict[str, Union[float, int]]]:
    """Prints: spikes, u, v for the first max_t timesteps."""
    neuron_dicts: List[Dict[str, Union[float, int]]] = []
    for snn in snns:
        neuron = snn.nodes[node_name]["nx_lif"][0]
        recurrent_weight = get_synapse_weight(
            snn=snn, left=node_name, right=node_name
        )
        a_in = get_synapse_weight(
            snn=snn, left=input_node_name, right=node_name
        )
        neuron_dicts.append(
            {
                "a_in": a_in,
                "a_in_time": a_in_time,
                "bias": neuron.bias.get(),
                "du": neuron.du.get(),
                "dv": neuron.dv.get(),
                "vth": neuron.vth.get(),
                "weight": recurrent_weight,
            }
        )
    return neuron_dicts


@typechecked
def drawProgressBar(
    percent: float, barLen: int, n_found: Optional[int] = None
) -> None:
    """Draws a completion bar."""
    sys.stdout.write("'\r'")
    progress = ""
    for i in range(0, barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    if n_found is not None:
        sys.stdout.write(
            f"[ {progress} ] {percent * 100:.2f}% (Found:{n_found} "
            + "satisfactory snns)."
        )
    else:
        sys.stdout.write(f"[ {progress} ] {percent * 100:.2f}%")
    sys.stdout.flush()


@typechecked
def get_synapse_weight(*, snn: nx.DiGraph, left: str, right: str) -> int:
    """Returns the weight of a synapse if it exists.

    Returns None otherwise.
    """
    if (left, right) in snn.edges():
        if "synapse" in snn.edges[(left, right)].keys():
            return snn.edges[(left, right)]["synapse"].weight
    return 0
