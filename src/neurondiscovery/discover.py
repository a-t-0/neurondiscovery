"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

import sys
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
from src.neurondiscovery.Discovery import Discovery
from src.neurondiscovery.print_behaviour import (
    drawProgressBar,
    print_found_neuron_behaviour,
)
from src.neurondiscovery.requirements.checker import (
    expected_spike_pattern_I,
    verify_input_spike,
    within_neuron_property_bounds,
)


@typechecked
def discover_neuron_type(*, disco: Discovery) -> None:
    """Create a particular configuration for the neuron Discovery algorithm."""
    max_time: int = 10000
    count = 0
    total = (
        len(disco.du_range)
        * len(disco.dv_range)
        * len(disco.vth_range)
        * len(disco.bias_range)
        * len(disco.weight_range)
        * len(disco.a_in_range)
    )
    print(f"du:{disco.du_range}")
    print(f"dv:{disco.dv_range}")
    print(f"bias:{disco.bias_range}")
    print(f"vth:{disco.vth_range}")
    print(f"weight:{disco.weight_range}")

    # pylint: disable=R1702
    for du in disco.du_range:
        for dv in disco.dv_range:
            for bias in disco.bias_range:
                for vth in disco.vth_range:
                    for weight in disco.weight_range:
                        for a_in in disco.a_in_range:
                            # Create neuron.
                            lif_neuron = LIF_neuron(
                                name="",
                                bias=float(bias),
                                du=float(du),
                                dv=float(dv),
                                vth=float(vth),
                            )
                            count = count + 1
                            drawProgressBar(percent=count / total, barLen=100)
                            # if count / total> 0.45:
                            (
                                is_expected,
                                snn_graph,
                            ) = create_snn(
                                lif_neuron=lif_neuron,
                                max_time=max_time,
                                weight=weight,
                                a_in=a_in,
                                a_in_time=disco.a_in_time,
                            )
                            if is_expected:
                                print_found_neuron_behaviour(
                                    snn_graph=snn_graph, t_max=50
                                )
                                print(f"du=       {du}")
                                print(f"dv=       {dv}")
                                print(f"vth=      {vth}")
                                print(f"bias=     {bias}")
                                print(f"weight=   {weight}")
                                print(f"a_in=     {a_in}")
                                print(f"a_in_time={disco.a_in_time}")
                                print("FOUND")
                                sys.exit()


@typechecked
def create_snn(
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

    return simulate_neuron(
        a_in_time=a_in_time,
        input_node_name=input_node_name,
        node_name=node_name,
        max_time=max_time,
        snn_graph=snn_graph,
    )


# pylint: disable=R0913


def simulate_neuron(
    a_in_time: Optional[int],
    input_node_name: str,
    node_name: str,
    max_time: int,
    snn_graph: nx.DiGraph,
) -> Tuple[bool, nx.DiGraph]:
    """Simulates the neuron."""
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
