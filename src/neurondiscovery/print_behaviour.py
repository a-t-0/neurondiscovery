"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

import sys
from typing import Union

import networkx as nx
from typeguard import typechecked


# pylint: disable=R0913
@typechecked
def print_found_neuron_behaviour(snn_graph: nx.DiGraph, t_max: int) -> None:
    """Prints: spikes, u, v for the first max_t timesteps."""
    for t in range(0, t_max):
        neuron = snn_graph.nodes["0"]["nx_lif"][t]
        print(f"{t},{neuron.spikes},u={neuron.u.get()},v={neuron.v.get()}")


@typechecked
def drawProgressBar(percent: float, barLen: int = 20) -> None:
    """Draws a completion bar."""
    sys.stdout.write("'\r'")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
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
