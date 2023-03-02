"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

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
    if a_in_time > 0:
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
def expected_spike_pattern_I(a_in_time: int, t: int) -> bool:
    """Specifies the expected spike pattern for neuron type I."""
    if t < 2 + a_in_time:
        return False
    return True


@typechecked
def within_neuron_property_bounds(lif_neuron: LIF_neuron) -> bool:
    """If the voltage exceeds 100, return False.."""
    if lif_neuron.v.get() > 100 or lif_neuron.v.get() < -100:
        return False
    if lif_neuron.u.get() > 100 or lif_neuron.u.get() < -100:
        return False
    return True
