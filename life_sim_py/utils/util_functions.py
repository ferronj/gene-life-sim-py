import numpy as np
import random


def random_position(size: tuple) -> np.array:
    x = random.randint(0, size[0])
    y = random.randint(0, size[1])
    return np.array([x, y])


def v_heading(x: float, y: float) -> float:
    # Return the angle in radians
    return np.arctan2(y, x)

def get_vector(position_1: np.array, position_2: np.array) -> np.array:
    dx = position_2[0] - position_1[0]
    dy = position_2[1] - position_1[1]
    return np.array([dx, dy])

def get_magnitude(vector: np.array) -> float:
    sum_squares = vector[0] ** 2 + vector[1] ** 2
    return np.sqrt(sum_squares)
