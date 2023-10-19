import numpy as np

from core.black_box import BlackBox


class Adder(BlackBox):
    def __init__(self, fs, chunks, n_input=2):
        super().__init__(fs, chunks)
        self._n_input = n_input

    def filter(self):
        out = np.zeros(self._chunks)

        for i in range(self._n_input):
            out += self._input_nodes[i].get_frame()

        # out = self._input_nodes[0].get_frame() + self._input_nodes[1].get_frame()

        self._output_node.set_frame(out)


class Gain(BlackBox):
    def __init__(self, gain, fs, chunks):
        super().__init__(fs, chunks)
        self._gain = gain

    def filter(self):
        out = self._gain * self._input_nodes[0].get_frame()
        self._output_node.set_frame(out)


class Mixer(BlackBox):
    def __init__(self, fs, chunks, n_input):
        super().__init__(fs, chunks)
        self._n_input = n_input

    def filter(self):
        res = 1
        for i in range(self._n_input):
            res *= self._input_nodes[i].get_frame()

        return res
