"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801

from typing import Dict, List, Optional, Union

import networkx as nx
from snnbackends.networkx.LIF_neuron import (
    LIF_neuron,
    print_neuron_properties_per_graph,
)
from snnbackends.networkx.run_on_networkx import (
    create_neuron_for_next_timestep,
    run_simulation_with_networkx_for_1_timestep,
)
from snnbackends.verify_graph_is_snn import verify_networkx_snn_spec
from typeguard import typechecked

from neurondiscovery.grid_settings.Discovery import Discovery
from neurondiscovery.search.create_snns import create_neurons, create_snns
from neurondiscovery.search.print_behaviour import (
    drawProgressBar,
    get_node_name_neuron_dicts,
    manage_printing,
)
from src.neurondiscovery.requirements.checker import (
    verify_input_spike,
    within_neuron_property_bounds,
)


@typechecked
def get_satisfactory_neurons(
    *,
    a_in_time: int,
    disco: Discovery,
    expected_spikes: List[bool],
    max_neuron_props: Dict[str, Union[float, int]],
    min_neuron_props: Dict[str, Union[float, int]],
    verbose: bool,
    print_behaviour: Optional[bool] = None,
    min_nr_of_neurons: Optional[int] = None,
) -> List[Dict[str, Union[float, int]]]:
    """Performs a run."""

    # Initialise properties.
    node_name: str = "0"
    input_node_name: str = "input_spike"

    # Create neurons.
    neurons: List[LIF_neuron] = create_neurons(disco=disco, verbose=verbose)
    if verbose:
        print(f"Created {len(neurons)} neurons")

    # Create snns.
    snns: List[nx.DiGraph] = create_snns(
        a_in_time=a_in_time,
        disco=disco,
        input_node_name=input_node_name,
        neurons=neurons,
        node_name=node_name,
    )
    if verbose:
        print(f"Created {len(snns)} snns.")

    working_snns: List[nx.DiGraph] = manage_simulation(
        a_in_time=a_in_time,
        expected_spikes=expected_spikes,
        input_node_name=input_node_name,
        node_name=node_name,
        max_neuron_props=max_neuron_props,
        min_neuron_props=min_neuron_props,
        snns=snns,
        verbose=verbose,
        min_nr_of_neurons=min_nr_of_neurons,
    )

    # Get neuron properties
    neuron_dicts: List[
        Dict[str, Union[float, int]]
    ] = get_node_name_neuron_dicts(
        a_in_time=a_in_time,
        input_node_name=input_node_name,
        node_name=node_name,
        snns=working_snns,
    )

    if verbose:
        manage_printing(
            expected_spikes=expected_spikes,
            neuron_dicts=neuron_dicts,
            node_name=node_name,
            working_snns=working_snns,
            print_behaviour=print_behaviour,
        )
    return neuron_dicts


# pylint: disable = R0913
@typechecked
def manage_simulation(
    a_in_time: int,
    expected_spikes: List[bool],
    input_node_name: str,
    node_name: str,
    max_neuron_props: Dict[str, Union[float, int]],
    min_neuron_props: Dict[str, Union[float, int]],
    snns: List[nx.DiGraph],
    verbose: bool,
    min_nr_of_neurons: Optional[int] = None,
) -> List[nx.DiGraph]:
    """Performs the neuron simulations for the snns."""

    working_snns: List[nx.DiGraph] = []

    # Simulate snns.
    for count, snn in enumerate(snns):
        if simulate_neuron(
            a_in_time=a_in_time,
            expected_spikes=expected_spikes,
            input_node_name=input_node_name,
            max_neuron_props=max_neuron_props,
            min_neuron_props=min_neuron_props,
            node_name=node_name,
            snn_graph=snn,
            verbose=verbose,
        ):
            working_snns.append(snn)
            print("Checking primary neuron:")
            print(
                get_node_name_neuron_dicts(
                    a_in_time=a_in_time,
                    input_node_name=input_node_name,
                    node_name=node_name,
                    snns=[snn],
                )
            )

        count = count + 1
        if verbose:
            drawProgressBar(
                percent=count / len(snns),
                barLen=100,
                n_found=len(working_snns),
            )
        if (
            min_nr_of_neurons is not None
            and len(working_snns) > min_nr_of_neurons
        ):
            break
    return working_snns


# pylint: disable=R0913
@typechecked
def simulate_neuron(
    a_in_time: int,
    expected_spikes: List[bool],
    input_node_name: str,
    max_neuron_props: Dict[str, Union[float, int]],
    min_neuron_props: Dict[str, Union[float, int]],
    node_name: str,
    snn_graph: nx.DiGraph,
    verbose: bool,
) -> bool:
    """Simulates the neuron."""
    # Simulate neuron for at most max_time timesteps, as long as it behaves
    # as desired.
    for t, expected_spike in enumerate(expected_spikes):
        # Copy the neurons into the new timestep.
        verify_networkx_snn_spec(snn_graph=snn_graph, t=t, backend="nx")
        create_neuron_for_next_timestep(snn_graph=snn_graph, t=t)
        verify_networkx_snn_spec(snn_graph=snn_graph, t=t + 1, backend="nx")

        neuron = snn_graph.nodes[node_name]["nx_lif"][t]
        if verbose:
            print(
                f"{t}:{neuron.spikes}, bias={neuron.bias.get()}, u="
                + f"{neuron.u.get()}, v={neuron.v.get()}, vth="
                + f"{neuron.vth.get()}"
            )

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
