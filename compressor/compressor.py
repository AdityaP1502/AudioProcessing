from core.cascaded_box import CascadedBox

from box.arithmetic import Mixer
from box.envelope_follower import EnvelopeFollower
from box.gain_reduction import GainReduction
from box.gain_smooth import GainSmooth

class Compressor(CascadedBox):
    def __init__(self, attack_time, release_time,
                 compressor_threshold, compressor_ratio, fs, chunks):

        super().__init__()

        self._mixer_component = Mixer(fs=fs, chunks=chunks, n_input=2)

        self._level_measurement = EnvelopeFollower(fs=fs, chunks=chunks)
        self._gain_smoother = GainSmooth(
          attack_time=attack_time,
          release_time=release_time,
          fs=fs,
          chunks=chunks,
        )

        self._gain_reducer = GainReduction(
          compressor_threshold=compressor_threshold,
          compressor_ratio=compressor_ratio,
          fs=fs,
          chunks=chunks
        )
    