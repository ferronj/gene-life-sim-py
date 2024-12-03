import pygame
import argparse

from life_sim_py.life_sim import run_simulation

parser = argparse.ArgumentParser()

parser.add_argument(
    "--generation",
    type=int,
    help="specify the starting generation number, useful when loading a previous generation from save",
    default=0,
)

parser.add_argument(
    "--num_generations",
    type=int,
    help="specify the number of generations to run the simulation, each successive generation will restart using initial config",
    default=5,
)

parser.add_argument(
    "--population_size",
    type=int,
    help="specify the number of cells to produce in each population",
    default=200,
)

parser.add_argument(
    "--auto_reset",
    type=bool,
    help="when population size drops to zero, generation a new population of size as specified",
    default=True,
)

parser.add_argument(
    "--load_from_save",
    type=str,
    dest='from_save',
    help="**UNUSED** Load a previous generation from a save file, specify the filepath",
    default=None,
)

parser.add_argument(
    "--print_config",
    type=bool,
    help="print run config details",
    default=False,
)


def run_life_sim():
    # Initialize Pygame
    pygame.init()

    args = parser.parse_args()

    # Call the GUI window function
    run_simulation(args)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    run_life_sim()
