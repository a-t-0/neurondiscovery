"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

from typing import List

import networkx as nx
from snnbackends.networkx.LIF_neuron import LIF_neuron, Synapse
from typeguard import typechecked

from neurondiscovery.src.neurondiscovery.grid_settings.Discovery import (
    Discovery,
)


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


@typechecked
def create_neurons(*, disco: Discovery, verbose: bool) -> List[LIF_neuron]:
    """Create a particular configuration for the neuron Discovery algorithm."""
    if verbose:
        print("")
        print(f"du:{disco.du_range}")
        print(f"dv:{disco.dv_range}")
        print(f"bias:{disco.bias_range}")
        print(f"vth:{disco.vth_range}")
        print(f"weight:{disco.weight_range}")

    neurons: List[LIF_neuron] = []
    # pylint: disable=R1702
    for du in disco.du_range:
        for dv in disco.dv_range:
            for bias in disco.bias_range:
                for vth in disco.vth_range:
                    # Create neuron.
                    neurons.append(
                        LIF_neuron(
                            name="",
                            bias=float(bias),
                            du=float(du),
                            dv=float(dv),
                            vth=float(vth),
                        )
                    )

    return neurons


@typechecked
def create_snns(
    *,
    a_in_time: int,
    disco: Discovery,
    input_node_name: str,
    neurons: List[LIF_neuron],
    node_name: str,
) -> List[nx.DiGraph]:
    """Creates a list of snns that are to be simulated."""
    snns: List[nx.DiGraph] = []
    for neuron in neurons:
        for weight in disco.weight_range:
            for a_in in disco.a_in_range:
                snns.append(
                    create_snn(
                        a_in=a_in,
                        a_in_time=a_in_time,
                        lif_neuron=neuron,
                        input_node_name=input_node_name,
                        node_name=node_name,
                        weight=weight,
                    )
                )
    return snns


@typechecked
def create_snn(
    *,
    a_in: float,
    a_in_time: int,
    node_name: str,
    input_node_name: str,
    lif_neuron: LIF_neuron,
    weight: int,
) -> nx.DiGraph:
    """Determines whether a neuron is of type I.

    Type I is arbitrarily defined as: 'does not spike for 2 timesteps,
    and then spikes indefinitely.'. (Because I would like to use such a
    neuron.).
    """

    snn_graph = nx.DiGraph()
    if a_in != 0:
        snn_graph.add_nodes_from(
            [node_name, input_node_name],
        )
        create_input_spike_neuron(
            a_in_time=a_in_time,
            a_in=a_in,
            input_node_name=input_node_name,
            node_name=node_name,
            snn_graph=snn_graph,
        )
    else:
        snn_graph.add_nodes_from(
            [node_name],
        )

    # Create tested neuron.
    snn_graph.nodes[node_name]["nx_lif"] = [lif_neuron]
    snn_graph.add_edges_from(
        [(node_name, node_name)],
        synapse=Synapse(
            weight=weight,
            delay=0,
            change_per_t=0,
        ),
    )

    return snn_graph
