"""
Module for implementation of comb filter
Comb filter is based on the feedback comb filter diagram[1]
[1]. https://www.dsprelated.com/freebooks/pasp/Feedback_Comb_Filters.html
"""

from core.cascaded_box import CascadedBox
from box.arithmetic import Adder, Gain
from box.delay import Delay

class CombFilter(CascadedBox):
    """
    A Class for creating a comb filter components. 
    This components is composed of a delay component, gain component, 
    and an adder component. The output of comb filter is taken from
    the adder output
    
    Attributes
    ----------
    _delay (float) : The amount of time (in seconds) the input line is delayed
    _gain (float) : Gain factor for the delay line
    _sample_rate (int) : The sample rate of the audio (in Hz)
    _chunks (int) : The number of samples per segment
    """

    def __init__(self, delay, gain, fs, chunks):
        super().__init__()

        self._delay = delay
        self._gain = gain
        self._sample_rate = fs
        self._chunks = chunks

        _delay_component = Delay(delay=delay, fs=fs, chunks=chunks)
        _gain_component = Gain(gain=-gain, fs=fs, chunks=chunks)
        _adder_component = Adder(fs=fs, chunks=chunks)

        _adder_component.insert_input_node(_gain_component.get_output_node())
        _gain_component.insert_input_node(_delay_component.get_output_node())
        _delay_component.insert_input_node(_adder_component.get_output_node())

        super().insert_components((1, _delay_component),
                                  (0, _adder_component), (2, _gain_component))
        super().set_output_node(_adder_component.get_output_node())

    def insert_input_node(self, node):
        """Insert input node into the components

        Args:
            node (Nodes): Input nodes
        """
        super().insert_input_node_to_component(node, 0)
