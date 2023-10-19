import numpy as np
from scipy.signal import firwin, fftconvolve

from core.black_box import BlackBox

class FIRFilter(BlackBox):
    def __init__(self, fs, chunks, wc=None, n_order=None, hn=None):
        super().__init__(fs, chunks)
        self._cutoff_freq = wc
        self._sample_rate = fs

        if hn is None:
            self._num_taps = n_order
            self._create_taps()

        else:
            self._num_taps = len(hn)
            self._taps = hn

        self._saved_input = np.zeros(self._num_taps - 1)

    def _create_taps(self):
        self._taps = firwin(
            self._num_taps,
            self._cutoff_freq,
            fs=self._sample_rate,
            pass_zero=True)

    def filter(self):
        # Filter using Overlap - Save
        # out = lfilter(self._taps, 1.0, self._input_nodes[0].get_frame())
        xn = self._input_nodes[0].get_frame()
        in1 = np.hstack((self._saved_input, xn))
        out = fftconvolve(in1, self._taps, mode="valid")

        assert len(out) == self._chunks, f"""Output length must equal
        to the chunk length. Received {len(out)}"""

        self._output_node.set_frame(out)

        # save M - 1 sample of current input
        self._saved_input[:] = xn[self._chunks - self._num_taps + 1:]
