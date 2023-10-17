from core.CascadedBox import CascadedBox
from box.Arithmetic import Adder, Gain
from Reverb.CombFilter import CombFilter

class AllPassFilter(CascadedBox):
  def __init__(self, delay, gain, fs, chunks):
    super().__init__()
    self._delay = delay
    self._gain = gain
    self._sample_rate = fs
    self._chunks = chunks

    _gain1_component = Gain(gain=-gain, fs=fs, chunks=chunks)
    _gain2_component = Gain(gain=1 - gain * gain, fs=fs, chunks=chunks)
    _adder_component = Adder(fs=fs, chunks=chunks)
    _comb_filter_component = CombFilter(delay=delay, gain=gain, fs=fs, chunks=chunks)

    _gain2_component.insert_input_node(_comb_filter_component.get_output_node())
    _adder_component.insert_input_node(_gain1_component.get_output_node())
    _adder_component.insert_input_node(_gain2_component.get_output_node())

    super().insert_components((0, _gain1_component), (1, _comb_filter_component), (2, _gain2_component), (3, _adder_component))
    super().set_output_node(_adder_component.get_output_node())

  def insert_input_node(self, node):
    super().insert_input_node(node, 0)
    super().insert_input_node(node, 1)