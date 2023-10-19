import numpy as np
from numba import jit

from time import time

from core.black_box import BlackBox

@jit(nopython=True)
def _smooth(x, prev_val, attack_constant, release_constant):
    if x < prev_val:
        return (1 - attack_constant) * x + attack_constant * prev_val
        
    return (1 - release_constant) * x + release_constant * prev_val
class GainSmooth(BlackBox):
    def __init__(self, attack_time: int, release_time: int, fs, chunks):
        super().__init__(fs, chunks)

        self._attack_constant = np.exp(-(1 / (fs * attack_time / 1000)))
        self._release_constant = np.exp(-(1 / (fs * release_time / 1000)))
        self._prev_gain : float = 1

    def filter(self):
        xn = self._input_nodes[0].get_frame()
        out = np.zeros_like(xn)
        for i, data in enumerate(xn):
            out[i] = _smooth(data, self._prev_gain, self._attack_constant,
                    self._release_constant)
            
            self._prev_gain = out[i]
        self._output_node.set_frame(out)
