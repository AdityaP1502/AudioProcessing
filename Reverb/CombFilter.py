from core.CascadedBox import CascadedBox
from box.Arithmetic import Adder, Gain
from box.Delay import Delay

class CombFilter(CascadedBox):
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

    super().insert_components((1, _delay_component), (0, _adder_component), (2, _gain_component))
    super().set_output_node(_adder_component.get_output_node())

  def insert_input_node(self, node):
    super().insert_input_node(node, 0)