"""
Implementation of tapped delay line. 
https://www.dsprelated.com/freebooks/pasp/Tapped_Delay_Line_TDL.html
"""
from core.cascaded_box import CascadedBox
from box.arithmetic import Adder, Gain
from box.delay import Delay

class TappedDelayLine(CascadedBox):
    def __init__(self, delay, gain, fs, chunks):
        super().__init__()

        assert len(delay) == len(gain), "Invalid delay \
        and gain length"

        # Component init
        _delay_comps = [
            (
                2 * i,
                Delay(
                    delay = delay[i] / 1000,
                    fs = fs,
                    chunks = chunks
                )
            ) for i in range(len(delay))
        ]

        _gain_comps = [
            (
                2 * i + 1,
                Gain(
                    gain=gain[i],
                    fs=fs,
                    chunks=chunks,
                )
            ) for i in range(len(gain))
        ]

        _adder_component = Adder(
            fs=fs,
            chunks=chunks,
            n_input=len(delay)
        )

        # assign input and output
        for (_delay, _gain) in zip(_delay_comps, _gain_comps):
            _gain[1].insert_input_node(_delay[1].get_output_node())

        for i, (_, _delay) in enumerate(_delay_comps[1:]):
            _delay.insert_input_node(_delay_comps[i][1].get_output_node())

        for _gain in _gain_comps:
            _adder_component.insert_input_node(_gain[1].get_output_node())


        super().set_output_node(_adder_component.get_output_node())

        # insert the components
        super().insert_components(*_delay_comps,
                                  *_gain_comps,
                                    (
                                        2 * len(delay),
                                        _adder_component
                                    ),
        )


    def get_tap(self, tap_id : int) :
        """Return the output node of the delay at the specified
        id  
        Args:
            tap_id (int): tha location of the tap. Tap id start from 0

        Returns:
            Nodes: The tap output node
        """

        return super().get_output_node(id=2 * tap_id + 1)

    def insert_input_node(self, node):
        super().insert_input_node_to_component(node, 0)

    