import numpy as np
from core.black_box import BlackBox

class Delay(BlackBox):
    def __init__(self, delay, fs, chunks):
        super().__init__(fs=fs, chunks=chunks)
        self._delay = delay
        self._sample_rate = fs
        self._chunks = chunks
        self._delay_sample = int(delay * fs)

        _sample = self._delay_sample + chunks
        self._mem = np.zeros(_sample)

    def _insert_into_delay_line(self, xn):
        assert len(xn) == self._chunks, f"Input length must be equal to the chunk length of {self._chunks}. Got {len(xn)}"
        self._mem[self._delay_sample:(self._delay_sample + self._chunks)] = xn

    def _roll_delay_line(self):
        self._mem = np.roll(self._mem, -self._chunks)

    def _get_delay_output(self):
        self._roll_delay_line()
        return self._mem[:self._chunks]

    def filter(self) -> np.ndarray:
        # return the sample stored in the memory and insert the new sample into
        # the memory
        delay_out = self._get_delay_output()
        self._insert_into_delay_line(self._input_nodes[0].get_frame())
        self._output_node.set_frame(delay_out)
