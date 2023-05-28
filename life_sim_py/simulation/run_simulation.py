import pygame
import random
import json
import pprint

from life_sim_py.utils.util_classes import ComplexEncoder

import life_sim_py.simulation.colors as colors
import life_sim_py.simulation.simulation_functions as sf


def run_simulation(args):
    # Initialize pygame
    pygame.init()

    # Set the window size
    screen_size = (700, 500)
    screen = pygame.display.set_mode(screen_size)

    # Set the title of the window
    pygame.display.set_caption("Life Sim Py v0.1")

    # Set the background color to black
    screen.fill(colors.black)

    # create environment objects
    energy_init = sf.init_environment_objects(
        count=1000,
        screen_dimensions=screen_size
        )
    
    block_init = sf.init_environment_objects(
        count=1000,
        screen_dimensions=screen_size
        )

    # Create initial population - this might get more complex as we add generations...
    # TODO: consider moving this to a separate function, population_functions?
    generation = args.generation

    population = sf.init_population(
        size=args.population_size,
        screen_dimensions=screen_size,
        generation=generation
        )

    print(args)
    if args.print_config:
        pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
        pp.pprint(population.reprJSON())

    # create environment dictionary
    environment = {
        'size': screen_size,
        'generation': generation,
        'cells': {
            'list': population.cells_list,
            'color': colors.green,
        },
        'energy': {
            'list': energy_init,
            'color': colors.blue
        },
        'block': {
            'list': block_init,
            'color': colors.yellow,
        },
        'signal': {
            'list': [],
            'color': colors.orange,
        },
        'waste': {
            'list': [],
            'color': colors.red,
        },
        'gene': {
            'list': [],
            'color': colors.purple,
        },
    }

    for key in environment:
        if isinstance(environment[key], dict):
            if key == 'cells':
                sf.draw_cells(
                    cells_list=environment[key]['list'],
                    surface=screen,
                    color=environment[key]['color']
                )
            else:
                sf.draw_chems(
                    chem_list=environment[key]['list'],
                    surface=screen,
                    color=environment[key]['color']
                    )

    # Update the display
    pygame.display.flip()

    # Set the maximum frame rate
    clock = pygame.time.Clock()

    # Run the game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif len(environment['cells']['list']) == 0 and args.auto_reset:
                generation += 1
                population = sf.init_population(size=args.population_size, screen_dimensions=environment['size'], generation=generation)
                environment['cells']['list'] = population.cells_list

        # Perform cell behaviors
        environment = sf.simulation_interactions(environment=environment)

        # Clear the screen
        screen.fill(colors.black)

        # Re-draw animations
        for key in environment:
            if isinstance(environment[key], dict):
                if key == 'cells':
                    sf.draw_cells(
                        cells_list=environment[key]['list'],
                        surface=screen,
                        color=environment[key]['color']
                    )
                else:
                    sf.draw_chems(
                        chem_list=environment[key]['list'],
                        surface=screen,
                        color=environment[key]['color']
                        )

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(10)

    # Exit pygame
    pygame.quit()
