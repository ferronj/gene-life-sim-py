import numpy as np
import random
import pygame
from datetime import date

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
from life_sim_py.population.population import Population


def init_environment_objects(
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
    size: int,
    screen_dimensions: tuple,
    generation: int = 0  # generation will feed to a population
) -> list[Cell]:

    date_id = date.today()
    pop_id = f'{size}_{date_id}_{generation}'

    population = Population(id=pop_id, size=size, generation=generation)

    for i in range(population.size):
        x = random.randint(0, screen_dimensions[0])
        y = random.randint(0, screen_dimensions[1])

        x_dir = random.uniform(-1, 1)
        y_dir = random.uniform(-1, 1)

        cell = Cell(
            id=f'{i}_{generation}',
            position=np.array([x, y]),
            position_vector=np.array([x_dir, y_dir])
        )

        population.cells_list.append(cell)

    return population


def simulation_interactions(environment: dict) -> dict:

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


