"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801
from typing import Optional, Tuple

import networkx as nx
from snnbackends.networkx.LIF_neuron import (
    LIF_neuron,
    Synapse,
    print_neuron_properties_per_graph,
)
from snnbackends.networkx.run_on_networkx import (
    create_neuron_for_next_timestep,
    run_simulation_with_networkx_for_1_timestep,
)
from snnbackends.verify_graph_is_snn import verify_networkx_snn_spec
from typeguard import typechecked

from src.neurondiscovery.create_input_neuron import create_input_spike_neuron


# pylint: disable=R0913
@typechecked
def is_expected_neuron_I(
    lif_neuron: LIF_neuron,
    max_time: int,
    weight: int,
    a_in: float,
    a_in_time: Optional[int] = None,
) -> Tuple[bool, nx.DiGraph]:
    """Determines whether a neuron is of type I.

    Type I is arbitrarily defined as: 'does not spike for 2 timesteps,
    and then spikes indefinitely.'. (Because I would like to use such a
    neuron.).
    """

    snn_graph = nx.DiGraph()
    node_name: str = "0"
    input_node_name: str = "input_spike"
    snn_graph.add_nodes_from(
        [node_name, input_node_name],
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

    create_input_spike_neuron(
        a_in_time=a_in_time,
        a_in=a_in,
        input_node_name=input_node_name,
        node_name=node_name,
        snn_graph=snn_graph,
    )

    # Simulate neuron for at most max_time timesteps, as long as it behaves
    # as desired.
    for t in range(0, max_time):
        # Copy the neurons into the new timestep.
        verify_networkx_snn_spec(snn_graph=snn_graph, t=t, backend="nx")
        create_neuron_for_next_timestep(snn_graph=snn_graph, t=t)

        verify_networkx_snn_spec(snn_graph=snn_graph, t=t + 1, backend="nx")
        # Simulate neuron.
        run_simulation_with_networkx_for_1_timestep(
            snn_graph=snn_graph, t=t + 1
        )
        verify_input_spike(
            a_in_time=a_in_time,
            input_node_name=input_node_name,
            snn_graph=snn_graph,
            t=t,
        )

        # If neuron behaves, continue, otherwise move on to next neuron.
        if snn_graph.nodes[node_name]["nx_lif"][
            t
        ].spikes != expected_spike_pattern_I(a_in_time=a_in_time, t=t):
            return False, snn_graph
        if not within_neuron_property_bounds(
            lif_neuron=snn_graph.nodes[node_name]["nx_lif"][t]
        ):
            return False, snn_graph

        if 100 < t < 150:
            print_neuron_properties_per_graph(
                G=snn_graph, static=False, t=t, neuron_type="nx_lif"
            )

    return True, snn_graph


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
