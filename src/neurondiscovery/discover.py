"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

from typing import Dict, List, Union

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
    get_synapse_weight,
    print_found_neuron_behaviour,
)
from src.neurondiscovery.requirements.checker import (
    verify_input_spike,
    within_neuron_property_bounds,
)


def manage_simulation(
    *,
    a_in_time: int,
    disco: Discovery,
    expected_spikes: List[bool],
    max_neuron_props: Dict[str, Union[float, int]],
    min_neuron_props: Dict[str, Union[float, int]],
) -> None:
    """Performs a run."""

    # Initialise properties.
    node_name: str = "0"
    input_node_name: str = "input_spike"
    working_snns: List[nx.DiGraph] = []

    # Create neurons.
    neurons: List[LIF_neuron] = create_neurons(disco=disco)
    snns: List[nx.DiGraph] = create_snns(
        a_in_time=a_in_time,
        disco=disco,
        input_node_name=input_node_name,
        neurons=neurons,
        node_name=node_name,
    )

    for count, snn in enumerate(snns):
        if simulate_neuron(
            a_in_time=a_in_time,
            expected_spikes=expected_spikes,
            input_node_name=input_node_name,
            max_neuron_props=max_neuron_props,
            min_neuron_props=min_neuron_props,
            node_name=node_name,
            snn_graph=snn,
        ):
            working_snns.append(snn)

        count = count + 1
        drawProgressBar(percent=count / len(snns), barLen=100)

    # Print found neurons
    print("")
    if len(working_snns) > 0:
        print("Found the following neurons that satisfy the requirements:")
    else:
        print("Did not find neurons that satisfy the requirements.")
    for count, working_snn in enumerate(working_snns):
        print_found_neuron_behaviour(snn_graph=working_snn, t_max=50)
        neuron = working_snn.nodes[node_name]["nx_lif"][0]
        recurrent_weight = get_synapse_weight(
            snn=working_snn, left=node_name, right=node_name
        )
        print(f"du=       {neuron.du.get()}")
        print(f"dv=       {neuron.dv.get()}")
        print(f"vth=      {neuron.vth.get()}")
        print(f"bias=     {neuron.bias.get()}")
        print(f"weight=   {recurrent_weight}")
        print("a_in=     TODO")
        print(f"a_in_time={disco.a_in_time}")


@typechecked
def create_neurons(*, disco: Discovery) -> List[LIF_neuron]:
    """Create a particular configuration for the neuron Discovery algorithm."""
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

    if a_in != 0:
        create_input_spike_neuron(
            a_in_time=a_in_time,
            a_in=a_in,
            input_node_name=input_node_name,
            node_name=node_name,
            snn_graph=snn_graph,
        )
    return snn_graph


# pylint: disable=R0913
def simulate_neuron(
    a_in_time: int,
    expected_spikes: List[bool],
    input_node_name: str,
    max_neuron_props: Dict[str, Union[float, int]],
    min_neuron_props: Dict[str, Union[float, int]],
    node_name: str,
    snn_graph: nx.DiGraph,
) -> bool:
    """Simulates the neuron."""
    # Simulate neuron for at most max_time timesteps, as long as it behaves
    # as desired.
    for t, expected_spike in enumerate(expected_spikes):
        # Copy the neurons into the new timestep.
        verify_networkx_snn_spec(snn_graph=snn_graph, t=t, backend="nx")
        create_neuron_for_next_timestep(snn_graph=snn_graph, t=t)
        verify_networkx_snn_spec(snn_graph=snn_graph, t=t + 1, backend="nx")

        # Simulate neuron.
        run_simulation_with_networkx_for_1_timestep(
            snn_graph=snn_graph, t=t + 1
        )

        # If an input spike is used, verify it behaves accordingly.
        # TODO: facilitate continuously spiking input.
        verify_input_spike(
            a_in_time=a_in_time,
            input_node_name=input_node_name,
            snn_graph=snn_graph,
            t=t,
        )

        # If neuron behaves, continue, otherwise move zon to next neuron.
        if snn_graph.nodes[node_name]["nx_lif"][t].spikes != expected_spike:
            return False
        if not within_neuron_property_bounds(
            lif_neuron=snn_graph.nodes[node_name]["nx_lif"][t],
            max_neuron_props=max_neuron_props,
            min_neuron_props=min_neuron_props,
        ):
            return False

        # If a neuron shows the expected behaviour for more than 100
        # timesteps, print its behaviour.
        if 100 < t < 150:
            print_neuron_properties_per_graph(
                G=snn_graph, static=False, t=t, neuron_type="nx_lif"
            )

    return True
