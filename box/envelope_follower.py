import numpy as np

from core.black_box import BlackBox


class EnvelopeFollower(BlackBox):
    def __init__(self, fs, chunks, attack_time=0.05, release_time=3):
        super().__init__(fs, chunks)

        self._attack_constant = np.exp(-2.2 / (44100 * attack_time / 1000))
        self._release_constant = np.exp(-2.2 / (44100 * release_time / 1000))

    def filter(self):
        frame = self._input_nodes[0].get_frame()
        out = np.zeros(len(frame))
        out[0] = np.abs(frame[0])

        for i in range(1, len(frame)):
            if np.abs(frame[i]) > frame[i - 1]:
                out[i] = (1 - self._attack_constant) * np.abs(frame[i]) + \
                    out[i - 1] * self._attack_constant
            else:
                out[i] = (1 - self._release_constant) * np.abs(frame[i]) + \
                    out[i - 1] * self._release_constant

        self._output_node.set_frame(out)
