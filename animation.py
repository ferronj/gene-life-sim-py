import pygame

import random

from life_sim_py.animation import colors
import life_sim_py.animation.animation_functions as af

# Initialize pygame
pygame.init()

# Set the window size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Life Sim Py v0.1")

# Set the background color to black
screen.fill(colors.black)

# create environment objects
energy = af.init_environment_objects(count=1000, screen_dimensions=size)
block = af.init_environment_objects(count=1000, screen_dimensions=size)

signal = []
waste = []
gene = []

cells = af.init_cells(count=50, screen_dimensions=size)

af.draw_chems(chem_list=energy, surface=screen, color=colors.grey)
af.draw_chems(chem_list=block, surface=screen, color=colors.grey)
af.draw_cells(cells_list=cells, surface=screen, color=colors.green)

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
    
    # Perform cell behaviors
    for cell in cells:
        cell.state['position'][0] += random.randint(-5, 5)
        cell.state['position'][1] += random.randint(-5, 5)
    
    # Clear the screen
    screen.fill(colors.black)
    
    # Re-draw animations
    af.draw_chems(chem_list=energy, surface=screen, color=colors.grey)
    af.draw_chems(chem_list=block, surface=screen, color=colors.grey)
    af.draw_chems(chem_list=signal, surface=screen, color=colors.grey)
    af.draw_chems(chem_list=waste, surface=screen, color=colors.grey)
    af.draw_chems(chem_list=gene, surface=screen, color=colors.grey)
    
    af.draw_cells(cells_list=cells, surface=screen, color=colors.green)

    # Update the display
    pygame.display.flip()
    
    # Limit the frame rate
    clock.tick(10)

# Exit pygame
pygame.quit()
