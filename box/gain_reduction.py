import numpy as np
from core.black_box import BlackBox

# @jit(nopython=True)
def _gain_calculation(x, threshold : float, ratio : float):
    y = np.ones_like(x)
    mask = x > threshold
    y[mask] = (threshold / x[mask]) ** (1 - 1 / ratio)
    return y

# cache the function
# _gain_calculation(1, 1, 1)

class GainReduction(BlackBox):
    def __init__(self, compressor_threshold, compressor_ratio, fs, chunks):
        super().__init__(fs, chunks)

        self._compressor_threshold = compressor_threshold
        self._compressor_ratio = compressor_ratio

    def filter(self):
        xn = self._input_nodes[0].get_frame()
        out = _gain_calculation(xn, self._compressor_threshold,
                                self._compressor_ratio)
        self._output_node.set_frame(out)
