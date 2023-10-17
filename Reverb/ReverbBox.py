from core.CascadedBox import CascadedBox
from box.Arithmetic import Adder
from Reverb.CombFilter import CombFilter
from filter.fir import FIRFilter
from Reverb.AllPassFilter import AllPassFilter

class ReverbBox(CascadedBox):
  def __init__(self, delay : list[int], gain : list[float], fs : int, chunks : int):
    super().__init__()
    
    assert len(delay) == len(gain) and len(delay) == 7, "Invalid length of delay and gain"
    
    # initiate components
    _fir_filter_component = FIRFilter(fs=fs, chunks=chunks, wc=3000, n_order=128)
    # _fir_filter2_component = FIRFilter(fs=fs, chunks=chunks, wc=7000, n_order=128)
    _all_pass_components = [(i + 5, AllPassFilter(delay=delay[i] / 1000, gain=gain[i], fs=fs, chunks=chunks)) for i in range(0, 3)]
    _comb_components = [(i - 3, CombFilter(delay=delay[i] / 1000, gain=gain[i], fs=fs, chunks=chunks)) for i in range(3, 7)]
    _adder_components = Adder(fs=fs, chunks=chunks, n_input=4)
    
    # connect the components
    for (_, _comb) in _comb_components:
      # _comb.insert_input_node(_all_pass_components[2][1].get_output_node())
      _adder_components.insert_input_node(_comb.get_output_node())

    _all_pass_components[0][1].insert_input_node(_adder_components.get_output_node())
    _all_pass_components[1][1].insert_input_node(_all_pass_components[0][1].get_output_node())
    _all_pass_components[2][1].insert_input_node(_all_pass_components[1][1].get_output_node())
    _fir_filter_component.insert_input_node(_all_pass_components[2][1].get_output_node())
    
    # _components = _all_pass_components + _comb_components + [(7, _adder_components)]
    super().insert_components(*_all_pass_components, (8, _fir_filter_component), *_comb_components, (4, _adder_components))
    
    # super().set_output_node(_all_pass_components[2][1].get_output_node())
    super().set_output_node(_fir_filter_component.get_output_node())
    # super().set_output_node(_fir_filter_component.get_output_node())
    
  def insert_input_node(self, node):
    # super().insert_input_node(node, 0)
    for i in range(4):
      super().insert_input_node(node, i)
      
  