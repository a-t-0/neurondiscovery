"""Contains the specification of and maximum values of the algorithm
settings."""
# pylint: disable=R0903
# pylint: disable=R0801
import sys

from snnbackends.networkx.LIF_neuron import LIF_neuron
from typeguard import typechecked

from src.neurondiscovery.Discovery import Discovery
from src.neurondiscovery.print_behaviour import (
    drawProgressBar,
    print_found_neuron_behaviour,
)
from src.neurondiscovery.requirements.checker import is_expected_neuron_I


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
                            ) = is_expected_neuron_I(
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
