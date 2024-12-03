import pygame
import pprint

from datetime import date

import life_sim_py.utils.colors as colors
import life_sim_py.sim_functions as sf


def run_simulation(args):
    # Initialize pygame
    pygame.init()

    # Set the window size
    screen_dimensions = (700, 500)
    screen = pygame.display.set_mode(screen_dimensions)

    # Set the title of the window
    pygame.display.set_caption("Life Sim Py v0.1")

    # Set the background color to black
    screen.fill(colors.black)

    # Create initial population - this might get more complex as we add generations...
    # TODO: consider moving this to a separate function, population_functions?
    date_id = date.today()
    generation = args.generation
    pop_size = args.population_size

    population = sf.init_population(
                    pop_size=pop_size,
                    screen_dimensions=screen_dimensions,
                    generation=generation
                    )

    print(args)
    if args.print_config:
        pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
        pp.pprint(population.reprJSON())

    #  create environment dictionary
    environment = sf.init_environment(
        pop_size=pop_size,
        date_id=date_id,
        generation=generation,
        screen_dimensions=screen_dimensions)

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
                population = sf.init_population(
                    pop_size=pop_size,
                    screen_dimensions=screen_dimensions,
                    generation=generation
                    )
                environment['cells']['list'] = population
                environment['cells']['tree'] = sf.create_cell_tree(
                                                    population=population,
                                                    property='position'
                                                    ),

        # Perform cell behaviors
        environment = sf.environment_interactions(environment=environment)

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
