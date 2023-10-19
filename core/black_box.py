from core.nodes import Nodes


class BlackBox():
    def __init__(self, fs, chunks):
        self._sample_rate = fs
        self._chunks = chunks
        self._input_nodes = []
        self._output_node = Nodes(chunks=chunks)

    def insert_input_node(self, node: Nodes):
        node.add_node_connection()
        self._input_nodes.append(node)

    def insert_output_node(self, node: Nodes):
        self._output_node = node

    def get_output_node(self):
        return self._output_node

    def filter(self):
        """
            This method do calculation on the given xn and produce a 
            new output with the same length. It will take frame from 
            input node by invokking Nodes class get_frame method. Then,
            the result is stored in the output node by invoking Nodes 
            class set_frame method.
        """
