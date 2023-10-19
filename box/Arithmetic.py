"""
Module for providing an implementation 
of basic arithmetic components
"""

import numpy as np

from core.black_box import BlackBox


class Adder(BlackBox):
    """ 
    A Class for creating an adder component instance. 
    This component take N component as input and produce one output. 
    The output is obtained by adding the frame given from all of the
    input node. 
    
    Attributes
    ----------
    _n_input (int) : The number of inputs (default is 2)
    _sample_rate (int) : The sample rate of the audio (in Hz)
    _chunks (int) : The number of samples per segment
    """

    def __init__(self, fs, chunks, n_input=2):
        super().__init__(fs, chunks)
        self._n_input = n_input

    def filter(self):
        """
        Add all of the input frame, from the input nodes then save the 
        output into the output node of the adder components. 
        """
        out = np.zeros(self._chunks)

        for i in range(self._n_input):
            out += self._input_nodes[i].get_frame()

        # out = self._input_nodes[0].get_frame() + self._input_nodes[1].get_frame()

        self._output_node.set_frame(out)


class Gain(BlackBox):
    """ 
    A Class for creating a gain component instance. 
    This component take one input node then output a multiplied version
    of the input frame by a factor of g.  
    
    Attributes
    ----------
    _gain (int) : The gain value (g)
    _sample_rate (int) : The sample rate of the audio (in Hz)
    _chunks (int) : The number of samples per segment
    """

    def __init__(self, gain, fs, chunks):
        super().__init__(fs, chunks)
        self._gain = gain

    def filter(self):
        """
        Multiply the input frame by a factor of g, 
        then save the result in the output node
        """

        out = self._gain * self._input_nodes[0].get_frame()
        self._output_node.set_frame(out)


class Mixer(BlackBox):
    """
    A Class for creating a mixer component instance. 
    This component take two input, then produce the mix result 
    by multiplying them together. 
    
    Attributes
    ----------
    _gain (int) : The gain value (g)
    _sample_rate (int) : The sample rate of the audio (in Hz)
    _chunks (int) : The number of samples per segment
    """

    def filter(self):
        """
        Multiply frame from the two input node together then saved
        the result in the output node
        """

        res = self._input_nodes[0].get_frame() * self._input_nodes[1].get_frame()
        self._output_node.set_frame(res)
