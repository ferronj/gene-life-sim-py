import random
import numpy as np

import life_sim_py.utils.util_functions as util

from life_sim_py.config.config_sim import (
    GENOME_MIN,
    GENOME_MAX,
    CELL_DETECTION_RADIUS
)

from life_sim_py.cells.genome import Genome, Network


class Cell():

    '''
    Cell object as foundation of the simulation. Contains genome information 
    and state information

    init:
    id: some unique identifier that is managed by the simulation
    position: np.array where the cell is located, either initialized randomly 
    from simulation init
        or created from a reproduction action of another cell
    position_vector: the direction the cell is facing, likely initialized 
    randomly

    State:
    self.genome: the genome object associated with this cell
    self.network: the actual neural network created by the genome
    self.state: real workhorse of the cell along with genome and network.
        position, position_vector, mass, potential, entropy, genome_length, 
        gene
    self.detected: a dictionary of items that have been detected by the cell 
        and is used for actions
        that influence state

    Methods:
    reprJSON: represent the cell in a JSON format for printing or pickle
    '''

    def __init__(
        self,
        id: str,
        position: list,
        position_vector: list,
        genome_length: int=None
    ) -> None:

        self.id = id

        # TODO: genome_length may not always be randomly generated...a 
        # reproduction event will specify
        # pass along a genome. Possibly just an optimization issue for later
        if genome_length is None:
            genome_length = random.randint(GENOME_MIN, GENOME_MAX)
        self.genome = Genome(genome_length)
        self.network = Network(self.genome.nodes)

        # Dataframe... I think the calculations are more efficient...
        # TODO: decide if this should be a dataframe or kept as a dict
        self.state = {
            'position': position,
            'position_vector': position_vector,
            'mass': 10,
            'potential': 100,
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

    def reprJSON(self):
        
        json_state = {
            'position': self.state['position'].tolist(),
            'position_vector': self.state['position_vector'].tolist(),
            'mass': self.state['mass'],
            'potential': self.state['potential'],
            'entropy': self.state['entropy'],
            'genome_length': self.state['genome_length'],
            'gene': []
        }
        
        json_dict = {
            'id': self.id,
            'state': json_state,
            'detected': self.detected,
            'genome': self.genome,
            'network': self.network
        }

        return json_dict

#  --------------------------------------------------------


def cell_id_match(cell_id,
                  environment: dict):
    # return the cell object from the environment that matches an id
    for cell in environment['cells']:
        if cell.id == cell_id:
            return cell


def get_sensor_value(
        input_id: str,
        cell: Cell,
        environment: dict
        ):
    '''
    get_sensor_value

    '''
    # get the cell from cell_id
    # cell = cell_id_match(
    #    cell_id=cell_id,
    #    environment=environment
    #    )
    
    if input_id == 'POSITION_X':
        # -1 to 1 distance from center
        x = environment['screen_dimensions'][0] / 2
        cell_x = cell.state['position'][0]

        return (cell_x - x) / x
    
    elif input_id == 'POSITION_Y':
        # -1 to 1 distance from center
        y = environment['screen_dimensions'][1] / 2
        cell_y = cell.state['position'][1]

        return (cell_y - y) / y
    
    elif input_id == 'POSITION_VECTOR':
        # radians around the circle
        x = cell.state['position'][0]
        y = cell.state['position'][1]

        return util.vector_to_heading(x, y)
    
    elif input_id == 'MASS':
        return cell.state['mass']
    

def consume_resource(
        resource_value: float,
        action_value: float
        ) -> tuple:
    
    # JF 121123: what is this doing?

    if resource_value > 0:
        resource_value = resource_value - action_value

        if resource_value < 0:
            action_value = action_value - np.abs(resource_value)
            resource_value = 0

    return resource_value, action_value


def identify_target_object():
    #  function to find an environment object to act on
    pass


# action_value input comes from the network output and is applied in 
# simulation functions environment_interactions and run in 
# run_simulation as part of the pygame run loop
def apply_action_output(
        output_id: str,
        action_value: float,
        cell: Cell,
        environment: dict
        ) -> dict:
    
    # cell = cell_id_match(
    #    cell_id=cell_id,
    #    environment=environment
    #    )

    if output_id == 'MOVE':
        
        resource_str = 'potential'

        cell.state[resource_str], action_value = consume_resource(
            resource_value=cell.state[resource_str],
            action_value=action_value
            )

        move_vector = cell.state['position_vector'] * action_value
        cell.state['position'] = cell.state['position'] + move_vector
        
        return environment
    
    elif output_id == 'TURN':
        
        resource_str = 'potential'

        cell.state[resource_str], action_value = consume_resource(
            resource_value=cell.state[resource_str],
            action_value=action_value
            )

        heading = util.vector_to_heading(
            x=cell.state['position_vector'][0],
            y=cell.state['position_vector'][1]
            )
        new_heading = heading * action_value
        cell.state['position_vector'] = util.heading_to_vector(new_heading)

        return environment

