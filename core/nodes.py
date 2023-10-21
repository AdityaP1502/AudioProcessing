"""
Implementation of node that will be used by components
to connect to other components, allowing for implementation 
of cascaded system. 
"""
import numpy as np


class Nodes():
    """
    A class for creating a node for connecting between components. 
    """
    
    def __init__(self, chunks):
        self._chunks = chunks
        self._frames = np.zeros(self._chunks)
        self._start = None
        self._n_nodes_connected = 0
        self._n_frame_used = 0

    def add_node_connection(self):
        """
        Add component that connect to this node
        """

        self._n_nodes_connected += 1

    def get_frame(self):
        if self._start is not None:
            t = self._start

            if self._n_frame_used == self._n_nodes_connected:
                self._start += self._chunks
                t = self._start
                self._n_frame_used = 0

            self._n_frame_used += 1
            return self._frames[t: t + self._chunks]

        return self._frames

    def set_frame(self, xn):
        assert len(xn) == self._chunks, "frame length invalid"
        self._frames = xn

    def set_frame_exceed_chunk_length(self, xn):
        """Use this when the frame length is very long

        Args:
            xn (np.ndarray): 1D numpy array.
        """

        self._start = 0
        self._frames = xn
