import numpy as np
import random
import pygame

from life_sim_py.constants.config_sim import (
    CHEM_DRAW_RADIUS
)

from life_sim_py.cell.cell import Cell


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


def init_cells(
    count: int,
    screen_dimensions: tuple
) -> list[Cell]:

    cells_list = []
    for i in range(count):
        x = random.randint(0, screen_dimensions[0])
        y = random.randint(0, screen_dimensions[1])

        x_dir = random.uniform(-1, 1)
        y_dir = random.uniform(-1, 1)

        cell = Cell(
            id=i,
            position=np.array([x, y]),
            position_vector=np.array([x_dir, y_dir])
        )

        cells_list.append(cell)

    return cells_list


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


