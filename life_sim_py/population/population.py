import numpy as np
import pandas as pd
import json

from life_sim_py.cell.cell import Cell
from life_sim_py.utils.util_classes import ComplexEncoder


# what does this class do....
# this is the connection to the outside work, how we view what's happening beyond the visuals
#
class Population():

    def __init__(
            self,
            id: int,
            size: int,
            generation: int = 0
            ) -> None:

        self.id = id
        self.size = size
        self.generation = generation
        self.cells_list = []

    def _init_population(self) -> None:
        pass

    def _save_population(self) -> None:
        pass

    def _load_population(self) -> None:
        pass

    def reprJSON(self):
        json_dict = {
            'id': self.id,
            'size': self.size,
            'cells': self.cells_list
        }
        return json_dict
