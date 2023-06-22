import numpy as np
import random
import pygame

from scipy.spatial import KDTree

from life_sim_py.config.config_sim import (
    CHEM_DRAW_RADIUS
)

from life_sim_py.cell.sensors_actions import (
    SENSORS,
    ACTIONS
)

from life_sim_py.cell.cell import (
    Cell,
    get_sensor_value,
    apply_action_output
)


#  KD Tree functions

def create_tree(
        object_list: list[tuple]
) -> KDTree:

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
) -> list[np.array]:

    object_list = []
    for _ in range(count):
        x = random.randint(0, screen_dimensions[0])
        y = random.randint(0, screen_dimensions[1])
        object_list.append(np.array([x, y]))

    return object_list


def init_population(
    pop_size: int,
    screen_dimensions: tuple,
    generation: int = 0  # generation will feed to a population
) -> list[Cell]:

    population = []

    for i in range(pop_size):
        x = random.randint(0, screen_dimensions[0])
        y = random.randint(0, screen_dimensions[1])

        x_dir = random.uniform(-1, 1)
        y_dir = random.uniform(-1, 1)

        cell = Cell(
            id=f'{i}_{generation}',
            position=np.array([x, y]),
            position_vector=np.array([x_dir, y_dir])
        )

        population.append(cell)

    return population


def init_environment():
    #  take this functionality out of run-simulation
    pass


def update_environment():
    #  take this functionality out of run-simulation
    pass


#  -------------- Simulation functions --------------

def environment_interactions(environment: dict) -> dict:

    for cell in environment['cells']['list']:
        # initialize the input array to the cell's network
        sensor_input = np.zeros(len(ACTIONS), dtype=float)
        
        # calculate sensor inputs from cell & environment
        for node in cell.network.nodes:
            if node['input_type'] == 'STATE':
                input_index = SENSORS.index(node['input_id'])
                sensor_input[input_index] += get_sensor_value(
                    input_id=node['input_id'],
                    cell_id=cell.id,
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
                    cell_id=cell.id,
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
    chem_list: list[np.array],
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
    cells_list: list[np.array],
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


