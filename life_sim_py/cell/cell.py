import random
import numpy as np

from life_sim_py.constants.config_sim import (
    GENOME_MIN,
    GENOME_MAX
)

from life_sim_py.cell.sensors_actions import (
    SENSORS,
    ACTIONS,
    get_sensor,
    get_action
)

from life_sim_py.genome.genome import Genome
from life_sim_py.genome.network import Network


class Cell():

    def __init__(
        self,
        id: int,
        position: np.array,
        position_vector: np.array
    ) -> None:

        self.id = id

        genome_length = random.randint(GENOME_MIN, GENOME_MAX)
        self.genome = Genome(genome_length)
        self.network = Network(self.genome.nodes)

        # Dataframe... I think the calculations are more efficient...
        self.state = {
            'position': position,
            'position_vector': position_vector,
            'mass': 10,
            'potential': 0,
            'entropy': 0,
            'genome_length': genome_length,
            'gene': []
            }

        self.detected = {
            'energy': [],
            'block': [],
            'signal': [],
            'waste': [],
            'gene': [],
            'cell': []
        }

    def _get_sensor_input(self) -> np.array:
        sensor_input = np.zeros(len(SENSORS))

    
    def _apply_action_output(self) -> None:

