import numpy as np

from life_sim_py.cell.sensors_actions import (
    SENSORS,
    ACTIONS
)

from life_sim_py.config.config_sim import NETWORK_INTERNAL_NODES


class Network():

    def __init__(
        self,
        nodes: list
    ) -> None:

        self.activation_func = np.tanh
        self.nodes = nodes

    def feed_forward(self, sensor_input: np.array) -> np.array:

        action_output = np.zeros(len(ACTIONS), dtype=float)
        internal_nodes = np.zeros(NETWORK_INTERNAL_NODES, dtype=float)

        for node in self.nodes:
            # capture only STATE inputs first
            # Send them to correct output array
            if node['input_type'] == 'STATE':
                input_index = SENSORS.index(node['input_id'])
                node_output = sensor_input[input_index] * node['weight']

                if node['output_type'] == 'STATE':
                    output_index = ACTIONS.index(node['output_id'])
                    action_output[output_index] += node_output
                else:
                    output_index = node['output_id']
                    internal_nodes[output_index] += node_output

        while sum(internal_nodes) > 0:
            # calculate actvation function
            layer_input = self.activation_func(internal_nodes)
            # reset internal nodes array
            internal_nodes = np.zeros(NETWORK_INTERNAL_NODES, dtype=int)
            # iterate through nodes and look for signal nodes only
            # send them to action output array or new internal output array
            for node in self.nodes:
                if node['input_type'] == 'SIGNAL':
                    input_index = node['input_id']
                    node_output = layer_input[input_index] * node['weight']

                    if node['output_type'] == 'STATE':
                        output_index = ACTIONS.index(node['output_id'])
                        action_output[output_index] += node_output
                    else:
                        output_index = node['output_id']
                        internal_nodes[output_index] += node_output

        network_output = self.activation_func(action_output)

        return network_output
    
    def _unit_step_func(self, x):

        activation = np.where(x >= 0, 1, 0)

        return activation
    
    def reprJSON(self):
        json_dict = {
            'activation_function': str(self.activation_func),
            'nodes': self.nodes
        }
        return json_dict

