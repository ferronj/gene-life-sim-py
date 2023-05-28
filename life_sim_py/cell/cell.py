import random
import numpy as np

import life_sim_py.utils.util_functions as util

from life_sim_py.config.config_sim import (
    GENOME_MIN,
    GENOME_MAX,
    CELL_DETECTION_RADIUS
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

    def reprJSON(self):
        
        json_state = {
            'position': self.state['position'],
            'position_vector': self.state['position_vector'],
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


def cell_id_match(cell_id, environment):
    for cell in environment['cells']['list']:
        if cell.id == cell_id:
            return cell


def get_sensor_value(
        input_id: str,
        cell_id: str,
        environment: dict
        ) -> float:
    
    # get the cell from cell_id
    cell = cell_id_match(
        cell_id=cell_id,
        environment=environment
        )
    
    if input_id == 'POSITION_X':
        # -1 to 1 distance from center
        x = environment['size'][0] / 2
        cell_x = cell.state['position'][0]

        return (cell_x - x) / x
    
    elif input_id == 'POSITION_Y':
        # -1 to 1 distance from center
        y = environment['size'][1] / 2
        cell_y = cell.state['position'][1]

        return (cell_y - y) / y
    
    elif input_id == 'POSITION_VECTOR':
        # radians around the circle
        x = cell.state['position'][0]
        y = cell.state['position'][1]

        return util.v_heading(x, y)
    
    elif input_id == 'MASS':
        return cell.state['mass']
    
    elif input_id == 'POTENTIAL':
        return cell.state['potential']
    
    elif input_id == 'ENTROPY':
        return cell.state['entropy']
    
    elif input_id == 'GENE':
        return len(cell.state['gene'])
    
    elif input_id == 'GENOME_LENGTH':
        return cell.state['genome_length']
    
    elif input_id == 'DETECT_ENERGY':
        detect = 0
        for chem in environment['energy']['list']:
            
            vector = util.get_vector(
                position_1=cell.state['position'],
                position_2=chem)
            
            d = util.get_magnitude(vector=vector)
            if d <= CELL_DETECTION_RADIUS:
                detect += 1
        return detect
    
    elif input_id == 'DETECT_BLOCK':
        detect = 0
        for chem in environment['block']['list']:
            
            vector = util.get_vector(
                position_1=cell.state['position'],
                position_2=chem)
            
            d = util.get_magnitude(vector=vector)
            if d <= CELL_DETECTION_RADIUS:
                detect += 1
        return detect
    
    elif input_id == 'DETECT_SIGNAL':
        detect = 0
        for chem in environment['signal']['list']:
            
            vector = util.get_vector(
                position_1=cell.state['position'],
                position_2=chem)
            
            d = util.get_magnitude(vector=vector)
            if d <= CELL_DETECTION_RADIUS:
                detect += 1
        return detect
    
    elif input_id == 'DETECT_WASTE':
        detect = 0
        for chem in environment['waste']['list']:
            
            vector = util.get_vector(
                position_1=cell.state['position'],
                position_2=chem)
            
            d = util.get_magnitude(vector=vector)
            if d <= CELL_DETECTION_RADIUS:
                detect += 1
        return detect
    
    elif input_id == 'DETECT_GENE':
        detect = 0
        for chem in environment['gene']['list']:
            
            vector = util.get_vector(
                position_1=cell.state['position'],
                position_2=chem)
            
            d = util.get_magnitude(vector=vector)
            if d <= CELL_DETECTION_RADIUS:
                detect += 1
        return detect
    
    elif input_id == 'DETECT_CELL':
        detect = 0
        for cell in environment['cells']['list']:
            
            vector = util.get_vector(
                position_1=cell.state['position'],
                position_2=cell.state['position']
                )
            
            d = util.get_magnitude(vector=vector)
            if d <= CELL_DETECTION_RADIUS:
                detect += 1
        return detect - 1  # don't count the cell we're working with
    
    elif input_id == 'DETECT_PHOTO':
        # no plan for this yet
        sensor_value = 0
        return sensor_value

    
def apply_action_output(
        output_id: str,
        action_value: float,
        cell_id: str,
        environment: dict
        ) -> dict:
    
    cell = cell_id_match(
        cell_id=cell_id,
        environment=environment
        )

    if output_id == 'MOVE':
        
        move_vector = cell.state['position_vector'] * action_value
        cell.state['position'] + move_vector
        
        return environment
    
    elif output_id == 'TURN':

        return environment
    
    elif output_id == 'GROW':

        return environment
    
    elif output_id == 'REPRODUCE':

        return environment
    
    elif output_id == 'DIE':

        return environment
    
    elif output_id == 'ATTACK':

        return environment
    
    elif output_id == 'ADD_GENE':

        return environment
    
    elif output_id == 'CUT_GENE':

        return environment
    
    elif output_id == 'TRANSPORT_IN_ENERGY':

        return environment
    
    elif output_id == 'TRANSPORT_IN_BLOCK':

        return environment
    
    elif output_id == 'TRANSPORT_IN_SIGNAL':

        return environment
    
    elif output_id == 'TRANSPORT_IN_WASTE':

        return environment
    
    elif output_id == 'TRANSPORT_IN_GENE':

        return environment
    
    elif output_id == 'TRANSPORT_OUT_ENERGY':
        
        return environment
    
    elif output_id == 'TRANSPORT_OUT_BLOCK':

        return environment
    
    elif output_id == 'TRANSPORT_OUT_SIGNAL':

        return environment
    
    elif output_id == 'TRANSPORT_OUT_WASTE':

        return environment
    
    elif output_id == 'TRANSPORT_OUT_GENE':

        return environment
    
    elif output_id == 'MASS_TO_POTENTIAL':

        return environment
    
    elif output_id == 'MASS_TO_ENTROPY':

        return environment
    
    elif output_id == 'POTENTIAL_TO_MASS':

        return environment
    
    elif output_id == 'POTENTIAL_TO_ENTROPY':

        return environment
    
    elif output_id == 'ENTROPY_TO_MASS':

        return environment
    
    elif output_id == 'ENTROPY_TO_POTENTIAL':

        return environment
    
    elif output_id == 'PHOTO_TO_POTENTIAL':

        return environment
    
    elif output_id == 'POTENTIAL_TO_PHOTO':

        return environment