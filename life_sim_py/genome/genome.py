import random

from life_sim_py.config.config_sim import (
    GENE_LENGTH,
    WEIGHT_BIT_SIZE
)

from life_sim_py.cell.sensors_actions import (
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
neuron weight (12-bit) scaled to a normal range pos/neg
"""


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

