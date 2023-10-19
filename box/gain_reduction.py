from util.Util import vectorize_method
from core.black_box import BlackBox

class GainReduction(BlackBox):
    def __init__(self, compressor_threshold, compressor_ratio, fs, chunks):
        super().__init__(fs, chunks)

        self._compressor_threshold = compressor_threshold
        self._compressor_threshold_squared = compressor_threshold ** 2
        self._compressor_ratio = compressor_ratio

    @vectorize_method
    def _gain_calculation(self, x):
        if self._compare(x):
            return (self._compressor_threshold /
                    x) ** (1 - 1 / self._compressor_ratio)

        return 1

    def filter(self):
        xn = self._input_nodes[0].get_frame()
        out = self._gain_calculation(xn)
        self._output_node.set_frame(out)
