import numpy as np

from core.black_box import BlackBox

class RMSLevelMeasure(BlackBox):
    def __init__(self, window_size, fs, chunks):
        super().__init__(fs, chunks)

        self._window_length = window_size * fs
        self._hop_length = int(self._window_length / 2)
        self._buffer = np.zeros(self._hop_length)

    def filter(self):
        xn = np.hstack((self._buffer, self._input_nodes[0].get_frame()))

        for i in range(0, len(xn) - self._window_length, self._hop_length):
            rms_squared = np.sqrt(np.mean(xn[i:i + self._window_length] ** 2))
            xn[i:i + self._window_length] = rms_squared

        self._output_node.set_frame(xn)
