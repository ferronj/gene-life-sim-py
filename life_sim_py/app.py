import pygame
import sys
import random

# Screen dimensions
WIDTH, HEIGHT = 700, 500
CELL_SIZE = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Button dimensions and positions
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 30
PAUSE_BUTTON_POS = (WIDTH - 180, 10)
RESET_BUTTON_POS = (WIDTH - 90, 10)

# Calculate the number of cells based on the screen size
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

def draw_grid(screen):
    """Draws the grid on the screen."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def populate_grid():
    """Creates a 2D list to represent the grid with random initial state."""
    return [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

def count_neighbors(grid, row, col):
    """Counts the number of live neighbors for a cell at (row, col)."""
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    count = 0
    for dr, dc in neighbors:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            count += grid[r][c]
    return count

def update_grid(grid):
    """Updates the grid according to Conway's Game of Life rules."""
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            live_neighbors = count_neighbors(grid, row, col)
            if grid[row][col] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[row][col] = 0  # Cell dies
                else:
                    new_grid[row][col] = 1  # Cell lives
            else:
                if live_neighbors == 3:
                    new_grid[row][col] = 1  # Cell becomes alive
    return new_grid

def draw_cells(screen, grid):
    """Draws the cells based on the grid data."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_buttons(screen, font):
    """Draws the Pause and Reset buttons on the screen."""
    pygame.draw.rect(screen, BUTTON_COLOR, (*PAUSE_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BUTTON_COLOR, (*RESET_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT))

    pause_text = font.render("Pause", True, BUTTON_TEXT_COLOR)
    reset_text = font.render("Reset", True, BUTTON_TEXT_COLOR)
    screen.blit(pause_text, (PAUSE_BUTTON_POS[0] + 10, PAUSE_BUTTON_POS[1] + 5))
    screen.blit(reset_text, (RESET_BUTTON_POS[0] + 10, RESET_BUTTON_POS[1] + 5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    font = pygame.font.Font(None, 24)  # Font for button text
    grid = populate_grid()  # Initialize grid with random values

    clock = pygame.time.Clock()
    running = True
    paused = False  # Track the pause state

    while running:
        screen.fill(BLACK)
        draw_grid(screen)
        draw_cells(screen, grid)
        draw_buttons(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if Pause button is clicked
                if PAUSE_BUTTON_POS[0] <= x <= PAUSE_BUTTON_POS[0] + BUTTON_WIDTH and PAUSE_BUTTON_POS[1] <= y <= PAUSE_BUTTON_POS[1] + BUTTON_HEIGHT:
                    paused = not paused  # Toggle pause state
                # Check if Reset button is clicked
                elif RESET_BUTTON_POS[0] <= x <= RESET_BUTTON_POS[0] + BUTTON_WIDTH and RESET_BUTTON_POS[1] <= y <= RESET_BUTTON_POS[1] + BUTTON_HEIGHT:
                    grid = populate_grid()  # Reset the grid with random values

        if not paused:
            grid = update_grid(grid)  # Update the grid for the next generation if not paused

        pygame.display.flip()
        clock.tick(10)  # Control the speed of updates (10 frames per second)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
