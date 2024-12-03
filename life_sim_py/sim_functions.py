import numpy as np
import random
import pygame

from datetime import date

from scipy.spatial import KDTree

import life_sim_py.utils.colors as colors

from life_sim_py.config.config_sim import (
    CHEM_DRAW_RADIUS
)

from life_sim_py.cells.sensors_actions import (
    SENSORS,
    ACTIONS
)

from life_sim_py.cells.cell import (
    Cell,
    get_sensor_value,
    apply_action_output
)


#  KD Tree functions

def create_tree(object_list: list[tuple]) -> KDTree:

    object_tree = KDTree(object_list)

    return object_tree


def create_cell_tree(population: list[Cell], property: str) -> KDTree:
    
    cell_list_by_property = [cell.state[property] for cell in population]
    cell_tree = KDTree(cell_list_by_property)

    return cell_tree


#  -------------- simulation initialize functions --------------

def init_environment_object_list(
    count: int,
    screen_dimensions: tuple
) -> list:

    object_list = []
    for _ in range(count):
        x = random.randint(0, screen_dimensions[0])
        y = random.randint(0, screen_dimensions[1])
        object_list.append(np.array([x, y]))

    return object_list


def init_population(
    pop_size: int,
    screen_dimensions: tuple,
    generation: int=0,  # generation will feed to a population
    genome_length: int=None
) -> list[Cell]:

    population = []

    for i in range(pop_size):
        x = random.randint(0, screen_dimensions[0])
        y = random.randint(0, screen_dimensions[1])

        x_dir = random.uniform(-1, 1)
        y_dir = random.uniform(-1, 1)

        if genome_length is None:
            cell = Cell(
                id=f'{i}_{generation}',
                position=np.array([x, y]),
                position_vector=np.array([x_dir, y_dir])
            )
        else:
            cell = Cell(
                id=f'{i}_{generation}',
                position=np.array([x, y]),
                position_vector=np.array([x_dir, y_dir]),
                genome_length=genome_length
            )

        population.append(cell)

    return population


def init_environment(
        pop_size: int,
        date_id: date,
        generation: int,
        screen_dimensions: tuple
        ):
    #  take this functionality out of run-simulation

    # create environment objects
    energy_list = init_environment_object_list(
        count=1000,
        screen_dimensions=screen_dimensions
        )
    
    block_list = init_environment_object_list(
        count=1000,
        screen_dimensions=screen_dimensions
        )
    
    population = init_population(
        pop_size=pop_size,
        screen_dimensions=screen_dimensions,
        generation=generation
        )

    environment = {
        'id': f'{pop_size}_{date_id}_{generation}',
        'screen_dimensions': screen_dimensions,
        'generation': generation,
        'cells': {
            'list': population,
            'tree': create_cell_tree(
                    population=population,
                    property='position'
                    ),
            'color': colors.green
        },
        'energy': {
            'list': energy_list,
            'tree': create_tree(energy_list),
            'color': colors.blue
        },
        'block': {
            'list': block_list,
            'tree': create_tree(block_list),
            'color': colors.yellow,
        },
        'signal': {
            'list': [],
            'tree': None,
            'color': colors.orange,
        },
        'waste': {
            'list': [],
            'tree': None,
            'color': colors.red,
        },
        'gene': {
            'list': [],
            'tree': None,
            'color': colors.purple,
        }
    }
    return environment


def update_environment():
    #  take this functionality out of run-simulation
    pass


#  -------------- Simulation functions --------------

def environment_interactions(environment: dict) -> dict:

    for cell in environment['cells']['list']:
        # initialize the input array to the cell's network
        sensor_input = np.zeros(len(SENSORS), dtype=float)
        
        # calculate sensor inputs from cell & environment
        for node in cell.network.nodes:
            if node['input_type'] == 'STATE':
                input_index = SENSORS.index(node['input_id'])
                sensor_input[input_index] += get_sensor_value(
                    input_id=node['input_id'],
                    cell=cell,
                    environment=environment
                    )
        
        # network feed forward, actually calculate the result
        network_output = cell.network.feed_forward(sensor_input)

        for node in cell.network.nodes:
            if node['output_type'] == 'STATE':
                output_index = ACTIONS.index(node['output_id'])
                
                environment = apply_action_output(
                    output_id=node['output_id'],
                    action_value=network_output[output_index],
                    cell=cell,
                    environment=environment
                    )

    return environment


def cell_entropy():
    pass


def cell_death():
    pass


def cell_reproduce():
    pass


#  -------------- Drawing functions --------------


def draw_chems(
    chem_list: list,
    surface: pygame.Surface,
    color: tuple
) -> None:

    for chem in chem_list:
        pygame.draw.circle(
            surface=surface,
            color=color,
            center=chem,
            radius=CHEM_DRAW_RADIUS
            )


def draw_cells(
    cells_list: list,
    surface: pygame.Surface,
    color: tuple
) -> None:

    for cell in cells_list:
        cell_radius = cell.state['mass'] / 10
        pygame.draw.circle(
            surface=surface,
            color=color,
            center=cell.state['position'],
            radius=cell_radius
            )


