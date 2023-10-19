class CascadedBox():
    def __init__(self):
        self._components = []
        self._output_node = None
        """
            When building a new cascaded system, build the component here, then
            call the insert_components method to assign the component to the class instance. 
          """

    def insert_components(self, *args):
        args = list(args)
        args.sort(key=lambda x: x[0])
        for (_, component) in args:
            self._components.append(component)

    def insert_input_node_to_component(self, node, component_id):
        self._components[component_id].insert_input_node(node)

    def get_output_node(self):
        if self._output_node is None:
            return self._components[-1].get_output_node

        return self._output_node

    def set_output_node(self, node):
        self._output_node = node

    def filter(self):
        for component in self._components:
            component.filter()
