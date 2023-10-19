import numpy as np
from numba import jit

from core.black_box import BlackBox


@jit(nopython=True)
def _smooth(x, prev_val, attack_constant, release_constant):
    if x > prev_val:
        return (1 - attack_constant) * x + attack_constant * prev_val
        
    return (1 - release_constant) * x + release_constant * prev_val

class EnvelopeFollower(BlackBox):
    def __init__(self, fs, chunks, attack_time=0.05, release_time=3):
        super().__init__(fs, chunks)

        self._attack_constant = np.exp(-2.2 / (44100 * attack_time / 1000))
        self._release_constant = np.exp(-2.2 / (44100 * release_time / 1000))

    def filter(self):
        frame = np.abs(self._input_nodes[0].get_frame())
        out = np.zeros_like(frame)
        prev_envelope = np.abs(frame[0])

        # s = time()
        for i, data in enumerate(frame[1:]):
            out[i + 1] = _smooth(data, prev_envelope, self._attack_constant,
                    self._release_constant)
            
            prev_envelope = out[i + 1]
                   
        # _ = _smooth(frame, out, prev_envelope, self._attack_constant, self._release_constant)
        # e = time()
        # print((e - s) * 1000, 'ms')
        
        self._output_node.set_frame(out)