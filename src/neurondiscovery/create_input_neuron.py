"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

import networkx as nx
from snnbackends.networkx.LIF_neuron import LIF_neuron, Synapse
from typeguard import typechecked


# pylint: disable=R0913
@typechecked
def create_input_spike_neuron(
    a_in_time: int,
    a_in: float,
    input_node_name: str,
    node_name: str,
    snn_graph: nx.DiGraph,
) -> None:
    """Creates an input spike neuron if a_in_time is larger than 0.

    If
    a_in_time== 0, then no input spike is given, nor verified.
    """
    # Create input neuron.
    input_neuron = LIF_neuron(
        name=input_node_name,
        bias=1.0,
        du=0.0,
        dv=0.0,
        vth=float(a_in_time - 1),
    )

    snn_graph.nodes[input_node_name]["nx_lif"] = [input_neuron]
    # Only add output spike edge if a_in_time is larger than 0.
    if a_in_time > 0:
        snn_graph.add_edges_from(
            [(input_node_name, node_name)],
            synapse=Synapse(
                weight=a_in,
                delay=0,
                change_per_t=0,
            ),
        )
    # Create inhibitory recurrent spike to silence after first spike.
    snn_graph.add_edges_from(
        [
            (
                input_node_name,
                input_node_name,
            )
        ],
        synapse=Synapse(
            weight=-10,
            delay=0,
            change_per_t=0,
        ),
    )
