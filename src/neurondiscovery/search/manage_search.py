"""Performs different neuron type searches, one for neurons with static
properties, and one for changing neuron properties."""
# If neuron properties already exist, load from file.
# TODO: support storing different neuron types under different names.
import os
from typing import Dict, List

from neurondiscovery.import_export import (
    load_dict_from_file,
    write_dict_to_file,
)
from neurondiscovery.Neuron_type import Neuron_type
from neurondiscovery.search.discover import get_satisfactory_neurons
from neurondiscovery.search.find_changing_neurons import (
    print_changing_neuron,
    spike_one_timestep_later_per_property,
)


def find_non_changing_neurons(
    neuron_type: Neuron_type, overwrite: bool
) -> Dict:
    """Finds neurons with static properties that show some spike pattern with
    and/or without input spikes.

    TODO: also verify pattern without input spike.
    """
    non_changing_filename: str = "static.json"
    output_filename: str = f"{neuron_type.type_dir}/{non_changing_filename}"
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
            verbose=True,
        )

        # Write neuron properties to file.
        write_dict_to_file(filepath=output_filename, neuron_dicts=neuron_dicts)

    return neuron_dicts


def find_changing_neurons(
    max_redundancy: int, neuron_type: Neuron_type, static_neurons: Dict
) -> List:
    """Finds neurons that show a spike pattern after changing 1 property with a
    delta value of 1, per timestep.

    In essence it is used to look for neurons that spike one time step later,
    *after/w.r.t. some input spike*, if you add +1 to some property.

    TODO: allow searching for max_redundancy for which a value is still found.
    TODO: include verification on changing a_in_time to see if the spike
    pattern shifts accordingly.
    """

    found_neurons: List = spike_one_timestep_later_per_property(
        a_in_time=neuron_type.a_in_time,
        neuron_dicts=static_neurons,
        max_redundancy=max_redundancy,
        wait_after_input=neuron_type.wait_after_input,
    )
    if len(found_neurons) == 0:
        print("Did not find suitable neuron.")
    else:
        for found_neuron in found_neurons:
            print("")
            print(f'Found for:{found_neuron["property"]} at:')
            print(found_neuron)
            print_changing_neuron(
                a_in_time=neuron_type.a_in_time,
                neuron_dict=found_neuron,
                the_property=found_neuron["property"],
                max_redundancy=max_redundancy,
                wait_after_input=neuron_type.wait_after_input,
            )

    changing_filename: str = "changing.json"
    output_filename: str = f"{neuron_type.type_dir}/{changing_filename}"
    write_dict_to_file(filepath=output_filename, neuron_dicts=found_neurons)

    return found_neurons
