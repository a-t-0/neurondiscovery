"""Performs different neuron type searches, one for neurons with static
properties, and one for changing neuron properties."""
# If neuron properties already exist, load from file.
# TODO: support storing different neuron types under different names.
import os
import sys
from pprint import pprint
from typing import Dict, List, Union

from typeguard import typechecked

from neurondiscovery.grid_settings.Custom_range import Custom_range
from neurondiscovery.grid_settings.Discovery import Discovery
from neurondiscovery.import_export import (
    load_dict_from_file,
    write_dict_to_file,
)
from neurondiscovery.neuron_types.Neuron_type import Neuron_type
from neurondiscovery.search.discover import get_satisfactory_neurons
from neurondiscovery.search.find_changing_neurons import (
    print_changing_neuron,
    spike_one_timestep_later_per_property,
)


@typechecked
def find_non_changing_neurons(
    neuron_type: Neuron_type, overwrite: bool, verbose: bool
) -> List[Dict[str, Union[float, int]]]:
    """Finds neurons with static properties that show some spike pattern with
    and/or without input spikes.

    TODO: also verify pattern without input spike.
    """
    non_changing_filename: str = "static.json"
    output_filename: str = f"{neuron_type.type_dir}/{non_changing_filename}"
    print(f"output_filename={output_filename}")
    if os.path.isfile(output_filename) and not overwrite:
        neuron_dicts = load_dict_from_file(output_filename)
    else:
        # if True:
        neuron_dicts = get_satisfactory_neurons(
            a_in_time=neuron_type.a_in_time,
            disco=neuron_type.grid_spec,
            expected_spikes=neuron_type.expected_spikes,
            # TODO: parameterise.
            max_neuron_props={"vth": 100},
            min_neuron_props={"vth": -100},
            min_nr_of_neurons=None,
            verbose=verbose,
        )

        # Write neuron properties to file.
        write_dict_to_file(filepath=output_filename, neuron_dicts=neuron_dicts)

    return neuron_dicts


# pylint: disable=W0719
# pylint: disable=R0913
@typechecked
def find_changing_neurons(
    max_redundancy: int,
    neuron_type: Neuron_type,
    print_verified_neurons: bool,
    static_neurons: List[Dict[str, Union[float, int]]],
    verify_shift: bool,
    verbose: bool,
) -> List[Dict[str, Union[int, float, str]]]:
    """Finds neurons that show a spike pattern after changing 1 property with a
    delta value of 1, per timestep.

    In essence it is used to look for neurons that spike one time step later,
    *after/w.r.t. some input spike*, if you add +1 to some property.

    TODO: allow searching for max_redundancy for which a value is still found.
    TODO: include verification on changing a_in_time to see if the spike
    pattern shifts accordingly.
    """
    print(f"neuron_type={neuron_type}")
    pprint(neuron_type.__dict__)

    found_neurons: List[
        Dict[str, Union[int, float, str]]
    ] = spike_one_timestep_later_per_property(
        neuron_dicts=static_neurons,
        neuron_type=neuron_type,
        max_redundancy=max_redundancy,
        wait_after_input=neuron_type.wait_after_input,
    )

    if verify_shift:
        for found_neuron in found_neurons:
            verify_changing_neuron(
                found_neuron=found_neuron,
                neuron_type=neuron_type,
                shift=10,
                verbose=verbose,
            )

    if print_verified_neurons:
        if len(found_neurons) == 0:
            print("Did not find suitable neuron.")
            sys.exit()
        else:
            for found_neuron in found_neurons:
                print("")
                print(f'Found for:{found_neuron["property"]} at:')
                pprint(found_neuron)
                print_changing_neuron(
                    a_in_time=neuron_type.a_in_time,
                    neuron_dict=found_neuron,
                    neuron_type=neuron_type,
                    the_property=found_neuron["property"],
                    max_redundancy=max_redundancy,
                    wait_after_input=neuron_type.wait_after_input,
                )

    changing_filename: str = "changing.json"
    output_filename: str = f"{neuron_type.type_dir}/{changing_filename}"
    write_dict_to_file(filepath=output_filename, neuron_dicts=found_neurons)

    return found_neurons


@typechecked
def verify_changing_neuron(
    found_neuron: Dict[str, Union[int, float, str]],
    neuron_type: Neuron_type,
    shift: int,
    verbose: bool,
) -> None:
    """Verifies that the expected spike pattern shifts in time along with
    a_in_time (increases).

    After finding a neuron loop over it with varying a_in_times to
    verify the properties still hold (and are not a lucky coincidence
    for a neuron that starts spiking around a_in_time=x anyways.)
    """
    # Copy neuron parameters into specific search range.
    print(f"found_neuron={found_neuron}")
    custom_range: Discovery = Custom_range(
        bias_range=[found_neuron["bias"]],
        du_range=[found_neuron["du"]],
        dv_range=[found_neuron["dv"]],
        vth_range=[found_neuron["vth"]],
        weight_range=[found_neuron["weight"]],
        a_in_range=[found_neuron["a_in"]],
        name="custom",
    )

    for i in range(1, shift):
        # Do a new static neuron search.
        local_neuron_type: Neuron_type = Neuron_type(
            a_in_time=neuron_type.a_in_time + i,
            grid_spec=custom_range,
            max_time=neuron_type.max_time,
            wait_after_input=neuron_type.wait_after_input,
            name="custom",
            spike_input_type=neuron_type.spike_input_type,
            spike_output_type=neuron_type.spike_output_type,
            output_dir=neuron_type.output_dir,
        )
        if verbose:
            pprint(local_neuron_type.__dict__)

        local_static_neurons = find_non_changing_neurons(
            neuron_type=local_neuron_type, overwrite=True, verbose=verbose
        )
        print(f"local_static_neurons={local_static_neurons}")

        # TODO: Assert the neuron is still behaving as expected.

        # Do a new changing neuron search.
        local_found_neurons: List[
            Dict[str, Union[int, float, str]]
        ] = find_changing_neurons(
            max_redundancy=4,
            neuron_type=local_neuron_type,
            print_verified_neurons=True,
            static_neurons=local_static_neurons,
            verify_shift=False,
            verbose=verbose,
        )

        # Update the a_in_time:
        if isinstance(local_found_neurons[0]["a_in_time"], int):
            local_found_neurons[0]["a_in_time"] -= i

        # Assert the neuron is still behaving as expected.
        if local_found_neurons[0] != found_neuron:
            print("local=")
            pprint(local_found_neurons[0])
            print("original=")
            pprint(found_neuron)
            raise ValueError(
                f"Error, after shifting a_in_time with:{i}, the same neuron "
                "was not found."
            )
