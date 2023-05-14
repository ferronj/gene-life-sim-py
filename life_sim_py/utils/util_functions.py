import numpy as np
import random


def random_position(size: tuple) -> np.array:
    x = random.randint(0, size[0])
    y = random.randint(0, size[1])
    return np.array([x, y])