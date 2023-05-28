import pygame
from life_sim_py.gui.gui_functions import GUIFunctions


# Scrapping GUI for now... pygame is funny... I don't know if I like it all that much...


def run_gui_window(args):
    # Initialize Pygame
    pygame.init()

    # Window dimensions
    window_width = 600
    window_height = 400

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (192, 192, 192)

    # Create the window
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Simulation GUI")

    # Button dimensions
    button_width = 150
    button_height = 30

    # Spacing
    button_spacing = 20

    # Positions
    start_button_x = (window_width - button_width) // 2
    start_button_y = (window_height - button_height * 4 - button_spacing * 3) // 2
    stop_button_x = start_button_x
    stop_button_y = start_button_y + button_height + button_spacing
    save_button_x = start_button_x
    save_button_y = stop_button_y + button_height + button_spacing
    quit_button_x = start_button_x
    quit_button_y = save_button_y + button_height + button_spacing

    # Font
    font = pygame.font.Font(None, 24)

    # GUI Functions instance
    gui_functions = GUIFunctions()

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check button clicks
                mouse_pos = pygame.mouse.get_pos()

                if start_button_x <= mouse_pos[0] <= start_button_x + button_width and start_button_y <= mouse_pos[1] <= start_button_y + button_height:
                    gui_functions.start_simulation(args)
                elif stop_button_x <= mouse_pos[0] <= stop_button_x + button_width and stop_button_y <= mouse_pos[1] <= stop_button_y + button_height:
                    gui_functions.stop_simulation()
                elif save_button_x <= mouse_pos[0] <= save_button_x + button_width and save_button_y <= mouse_pos[1] <= save_button_y + button_height:
                    gui_functions.save_population()
                elif quit_button_x <= mouse_pos[0] <= quit_button_x + button_width and quit_button_y <= mouse_pos[1] <= quit_button_y + button_height:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))  # Send pygame.QUIT event

        # Clear the window
        window.fill(white)

        # Draw buttons
        pygame.draw.rect(window, gray, (start_button_x, start_button_y, button_width, button_height))
        pygame.draw.rect(window, gray, (stop_button_x, stop_button_y, button_width, button_height))
        pygame.draw.rect(window, gray, (save_button_x, save_button_y, button_width, button_height))
        pygame.draw.rect(window, gray, (quit_button_x, quit_button_y, button_width, button_height))

        # Draw button labels
        start_label = font.render("Start Simulation", True, black)
        stop_label = font.render("Stop Simulation", True, black)
        save_label = font.render("Save Population", True, black)
        quit_label = font.render("Quit", True, black)

        window.blit(start_label, (start_button_x + 10, start_button_y + 5))
        window.blit(stop_label, (stop_button_x + 10, stop_button_y + 5))
        window.blit(save_label, (save_button_x + 10, save_button_y + 5))
        window.blit(quit_label, (quit_button_x + 10, quit_button_y + 5))

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()
