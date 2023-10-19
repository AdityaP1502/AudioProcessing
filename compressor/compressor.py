from core.cascaded_box import CascadedBox
from box.arithmetic import Mixer
from box.envelope_follower import EnvelopeFollower
from box.gain_reduction import GainReduction
from box.gain_smooth import GainSmooth

class Compressor(CascadedBox):
    """
    A class that create a compressor component. The compressor comprised of a level 
    measurer, a gain reducer, and a gain smoother. Level measurer that this class used
    is an envelope follower.   
    """
    def __init__(self, attack_time, release_time,
                 compressor_threshold, compressor_ratio, fs, chunks):

        super().__init__()

        _mixer_component = Mixer(
            fs=fs,
            chunks=chunks
        )

        _level_measurement = EnvelopeFollower(
            fs=fs,
            chunks=chunks
        )

        _gain_smoother = GainSmooth(
          attack_time=attack_time,
          release_time=release_time,
          fs=fs,
          chunks=chunks,
        )

        _gain_reducer = GainReduction(
          compressor_threshold=compressor_threshold,
          compressor_ratio=compressor_ratio,
          fs=fs,
          chunks=chunks
        )

        _gain_reducer.insert_input_node(_level_measurement.get_output_node())
        _gain_smoother.insert_input_node(_gain_reducer.get_output_node())
        _mixer_component.insert_input_node(_gain_smoother.get_output_node())

        super().insert_components(
            (0, _level_measurement),
            (1, _gain_reducer),
            (2, _gain_smoother),
            (3, _mixer_component)
        )
     
        super().set_output_node(_mixer_component.get_output_node())

    def insert_input_node(self, node):
        super().insert_input_node_to_component(node, 0)
        super().insert_input_node_to_component(node, 3)

    