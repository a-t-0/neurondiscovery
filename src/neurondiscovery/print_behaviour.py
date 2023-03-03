"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

import sys
from typing import List, Optional, Union

import networkx as nx
from typeguard import typechecked


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
def print_neuron_properties(
    *,
    a_in_time: int,
    input_node_name: str,
    node_name: str,
    snns: List[nx.DiGraph],
) -> None:
    """Prints: spikes, u, v for the first max_t timesteps."""
    for snn in snns:
        neuron = snn.nodes[node_name]["nx_lif"][0]
        recurrent_weight = get_synapse_weight(
            snn=snn, left=node_name, right=node_name
        )
        a_in = get_synapse_weight(
            snn=snn, left=input_node_name, right=node_name
        )
        print(
            f"du={neuron.du.get()}, dv={neuron.dv.get()}, vth="
            + f"{neuron.vth.get()}, bias={neuron.bias.get()}, weight="
            + f"{recurrent_weight}, a_in={a_in}, a_in_time={a_in_time}"
        )


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
def get_synapse_weight(
    *, snn: nx.DiGraph, left: str, right: str
) -> Union[None, int]:
    """Returns the weight of a synapse if it exists.

    Returns None otherwise.
    """
    if (left, right) in snn.edges():
        if "synapse" in snn.edges[(left, right)].keys():
            return snn.edges[(left, right)]["synapse"].weight
    return None
