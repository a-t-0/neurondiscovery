"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

from typing import Dict, Union

import networkx as nx
from snnbackends.networkx.LIF_neuron import LIF_neuron
from typeguard import typechecked


@typechecked
def verify_input_spike(
    a_in_time: int,
    input_node_name: str,
    snn_graph: nx.DiGraph,
    t: int,
) -> None:
    """Raises exception if input neuron does not spike once at a_in_time."""
    if input_node_name in snn_graph.nodes():
        if t == a_in_time:
            if not snn_graph.nodes[input_node_name]["nx_lif"][t].spikes:
                raise SyntaxError(
                    "Error, the input neuron did not spike, at the "
                    f"a_in_time={a_in_time}. t={t}"
                )
        elif snn_graph.nodes[input_node_name]["nx_lif"][t].spikes:
            raise SyntaxError(
                "Error, the input neuron spiked, at the "
                f"a_in_time={a_in_time}. t={t}"
            )


@typechecked
def within_neuron_property_bounds(
    lif_neuron: LIF_neuron,
    max_neuron_props: Dict[str, Union[float, int]],
    min_neuron_props: Dict[str, Union[float, int]],
) -> bool:
    """Checks whether the neuron properties are within the specified bounds.

    E.g. if the voltage exceeds 100, return False, else return True.
    """
    for attr, min_val in min_neuron_props.items():
        if getattr(lif_neuron, attr).get() < min_val:
            return False
    for attr, max_val in max_neuron_props.items():
        if getattr(lif_neuron, attr).get() > max_val:
            return False
    return True
