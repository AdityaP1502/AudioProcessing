"""
Implementation of the foundation of components. 
"""

from core.nodes import Nodes

class BlackBox():
    """
    A class for providing the foundation for components. 
    
    Attributes
    ---
    _sample_rate (int) : Sample rate (in Hz). 
    _chunks (int) : Num of samples in each segment. 
    _input_nodes (list[Nodes]) : list of input nodes
    _output_node (Nodes) : Output node of the components
    """

    def __init__(self, fs, chunks):
        self._sample_rate = fs
        self._chunks = chunks
        self._input_nodes = []
        self._output_node = Nodes(chunks=chunks)

    def insert_input_node(self, node: Nodes):
        """Insert input node into the components

        Args:
            node (Nodes): Input node. 
        """

        node.add_node_connection()
        self._input_nodes.append(node)

    def insert_output_node(self, node: Nodes):
        """Insert output node into the components

        Args:
            node (Nodes): Input node. 
        """

        self._output_node = node

    def get_output_node(self):
        """Return the output node assigned to the component

        Returns:
            Nodes : Output node
        """

        return self._output_node

    def filter(self):
        """
            This method do calculation on the given xn and produce a 
            new output with the same length. It will take frame from 
            input node by invokking Nodes class get_frame method. Then,
            the result is stored in the output node by invoking Nodes 
            class set_frame method.
        """
