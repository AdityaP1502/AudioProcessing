import numpy as np

from util.Util import vectorize_method
from core.black_box import BlackBox


class GainSmooth(BlackBox):
    def __init__(self, attack_time: int, release_time: int, fs, chunks):
        super().__init__(fs, chunks)

        self._AT = np.exp(-(1 / (fs * attack_time / 1000)))
        self._RT = np.exp(-(1 / (fs * release_time / 1000)))
        self._prev_gain = 1

    @vectorize_method
    def _smoothing(self, x):
        if x < self._prev_gain:
            return (1 - self._AT) * x + self._AT * self._prev_gain

        return (1 - self._RT) * x + self._RT * self._prev_gain

    def filter(self):
        xn = self._input_nodes[0].get_frame()
        out = self._smoothing(xn)
        self._prev_gain = out[-1]

        self._output_node.set_frame(out)
