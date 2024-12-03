import random
import numpy as np

from life_sim_py.config.config_sim import (
    GENE_LENGTH,
    WEIGHT_BIT_SIZE,
    NETWORK_INTERNAL_NODES
)

from life_sim_py.cells.sensors_actions import (
    SENSORS,
    ACTIONS,
)

"""
input --> neuron --> output

inputs and outputs can be a STATE (0) or a SIGNAL (1)

3 Neuron types
SENSOR:
    - input STATE information from the cell
    - output a SIGNAL about that information
INTERNAL:
    - input a SIGNAL from a sensor or internal neuron
    - ouput a SIGNAL to an action or internal neuron
ACTION:
    - input a SIGNAL from sensor or internal neuron
    - output STATE information to the cell (movement, age, health, attack)
REFLEX:
    - input STATE information
    - ouput STATE information

...uncertain if REFLEX provides value. Two likely scenarios:
    1. The net balance of weights across the network balances out
        ...reflex and sensor-action pairs behave the comparably
    2. REFLEX

Genes describe neuron connections and the weight of the connection:
input type (1-bit) 0=STATE, 1=SIGNAL
input id (5-bit)  % len(neurons) gives index of relevent neurons
output type (1-bit) 0=STATE, 1=SIGNAL
output id (5-bit) % len(neurons) gives index of relevent neurons
neuron weight (12-bit) scaled to a normal range pos/neg (size given by global variable in config_sim.py)
"""


def analyze_genome_parameters(start_code, stop_code):
    genomes = []
    for i in range(100):
        genomes.append(create_random_genome(stop_code))

    sum = 0
    count = 0
    start_idx = []
    start_count = 0

    for g in genomes:
        sum += len(g)
        count += 1
        start_loc = search_binary_string(g, start_code)
        start_idx.append(start_loc)
        start_count += len(start_loc)

    mean = sum / count
    mean_start = start_count / count

    print(f'mean genome length: {mean}; mean genes per genome: {mean_start}')


def split_genome(genome, start_code, stop_code):
    # init genes list
    gene_list = []
    # cut the stop codon out of genome
    stop_length = len(stop_code)
    genome_ = genome[:-stop_length]
    # get indices of all start code locations
    gene_starts = search_binary_string(genome_, start_code)
    for idx, start_idx in enumerate(gene_starts):
        if idx < len(gene_starts) - 1:
            # start the genome slice after the start_code
            slice_start = start_idx + len(start_code)
            # end the slice at index of next gene start code
            slice_end = gene_starts[idx + 1]
            gene = genome_[slice_start:slice_end]
            # only append genes with sequences
            if len(gene) > 0:
                gene_list.append(gene)
    return gene_list
    
######################################################################

def create_random_genome(stop_code):
    write_genome = True
    genome = str(random.randint(0, 1))
    while write_genome:
        genome += str(random.randint(0, 1))
        if stop_code in genome:
            write_genome = False
    return genome


def search_binary_string(binary_string, sequence):
    positions = []
    index = binary_string.find(sequence)
    while index != -1:
        positions.append(index)
        index = binary_string.find(sequence, index+len(sequence))
    return positions

def create_random_gene(gene_length):
    gene = str(random.randint(0, 1))
    for _ in range(gene_length-1):
        gene += str(random.randint(0, 1))
    return gene


def read_gene(gene) -> dict:
    weight_idx = -WEIGHT_BIT_SIZE

    gene_ = {
        'input_type': int(gene[0], 2),
        'input_id': int(gene[1:6], 2),
        'output_type': int(gene[6], 2),
        'output_id': int(gene[7:12], 2),
        'weight': gene[weight_idx:]
    }

    weight_scalar = 2 ** (WEIGHT_BIT_SIZE - 1)

    # first bit of the weight region defines pos/neg
    if int(gene_['weight'][0], 2) == 0:
        weight_int = -1 * int(gene_['weight'][1:], 2)
    else:
        weight_int = int(gene_['weight'][1:], 2)

    gene_['weight'] = (weight_int / weight_scalar) ** 3

    return gene_


def random_bit_flip(genome):
    random_bit = random.randint(0, len(genome)-1)
    if int(genome[random_bit]) == 0:
        genome[random_bit] = 1
    else:
        genome[random_bit] = 0
    return genome


class Genome():

    gene_length = GENE_LENGTH

    def __init__(
        self,
        genome_length
    ) -> None:

        self.genome_length = genome_length
        self.genome = self._create_random_genome()
        self.nodes = self._read_genome()

    def _create_random_genome(self) -> list:
        genome = []
        for _ in range(self.genome_length):
            genome.append(create_random_gene(self.gene_length))
        return genome

    def _read_genome(self) -> list:

        nodes = []
        for gene in self.genome:
            nodes.append(read_gene(gene))

        for idx, node in enumerate(nodes):
            if node['input_type'] == 0:
                node['input_type'] = 'STATE'
                input_idx = node['input_id'] % len(SENSORS)
                node['input_id'] = SENSORS[input_idx]
            else:
                node['input_type'] = 'SIGNAL'

            if node['output_type'] == 0:
                node['output_type'] = 'STATE'
                output_idx = node['output_id'] % len(ACTIONS)
                node['output_id'] = ACTIONS[output_idx]
            else:
                node['output_type'] = 'SIGNAL'

            if (node['input_type'] == 'SIGNAL' and
                    node['output_type'] == 'SIGNAL'):

                if node['input_id'] == node['output_id']:
                    del nodes[idx]

        return nodes

    def reprJSON(self):
        json_dict = {
            'genome': self.genome
        }
        return json_dict


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


