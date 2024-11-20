"""
player.py

This module provides the user interface for interacting with the Sudoku solver.
It uses Pygame to create a visual representation of the Sudoku board, allowing the user to:
- Input initial board values manually.
- Solve the board using the integrated solver.
- Reset the board to start over.

The interface includes controls for navigation (arrow keys), number input, and buttons for solving and resetting the board.
"""

import pygame
import sys
from solver import Board, Solver  # Importing the Board and Solver classes

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Define dimensions
WIDTH = 800  # Width of the window
HEIGHT = 650  # Height of the window to leave space for instructions and button
GRID_SIZE = 60  # Size of each cell

# Define offsets for the board
BOARD_X_OFFSET = 20  # Start 20 pixels from the left
BOARD_Y_OFFSET = 20  # Start 20 pixels from the top

# Define button for the window
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Create a Pygame window and draw the Sudoku grid
def draw_grid(screen, board):
    """
    Draw the Sudoku grid and its current state on the given Pygame screen.

    Args:
        screen (pygame.Surface): The Pygame screen on which to draw the Sudoku grid.
        board (Board): An instance of the Board class that represents the current Sudoku board state.

    The function fills the screen with a white background, draws a 9x9 Sudoku grid with lines to separate 
    cells and subgrids, and displays any numbers already filled in the cells.
    """

    # Fill background with white
    screen.fill(WHITE)

    # Draw the grid lines
    for row in range(10):
        if row % 3 == 0:  # Thicker lines for subgrids
            pygame.draw.line(screen, BLACK,
                             (BOARD_X_OFFSET, BOARD_Y_OFFSET + row * GRID_SIZE),
                             (BOARD_X_OFFSET + 9 * GRID_SIZE, BOARD_Y_OFFSET + row * GRID_SIZE), 4)
                                # Start and end of the line (x,y)
        else:
            pygame.draw.line(screen, BLACK,
                             (BOARD_X_OFFSET, BOARD_Y_OFFSET + row * GRID_SIZE),
                             (BOARD_X_OFFSET + 9 * GRID_SIZE, BOARD_Y_OFFSET + row * GRID_SIZE), 1)

    for col in range(10):
        if col % 3 == 0:  # Thicker lines for subgrids
            pygame.draw.line(screen, BLACK,
                             (BOARD_X_OFFSET + col * GRID_SIZE, BOARD_Y_OFFSET),
                             (BOARD_X_OFFSET + col * GRID_SIZE, BOARD_Y_OFFSET + 9 * GRID_SIZE), 4)
        else:
            pygame.draw.line(screen, BLACK,
                             (BOARD_X_OFFSET + col * GRID_SIZE, BOARD_Y_OFFSET),
                             (BOARD_X_OFFSET + col * GRID_SIZE, BOARD_Y_OFFSET + 9 * GRID_SIZE), 1)

    # Draw the numbers on the grid
    font = pygame.font.Font(None, 42)
    for row in range(9):
        for col in range(9):
            if board.grid[row][col] != 0:
                value = board.grid[row][col]
                text = font.render(str(value), True, BLACK)
                # Draw numbers in the cells with offsets applied
                screen.blit(text, (BOARD_X_OFFSET + col * GRID_SIZE + GRID_SIZE // 3,
                                   BOARD_Y_OFFSET + row * GRID_SIZE + GRID_SIZE // 4))

# Draw instructions on the screen
def draw_instructions(screen):
    """
    Draw the user instructions on the given Pygame screen.

    Args:
        screen (pygame.Surface): The Pygame screen on which to draw the instructions.

    The function displays a set of user instructions for interacting with the Sudoku board, including
    navigation keys, input keys, and the solve/reset options. The instructions are drawn beside the board.
    """

    font = pygame.font.Font(None, 18)
    instructions = [
        "Use arrow keys to navigate cells.",
        "Press numbers 1-9 to fill cells.",
        "Press 0 or BACKSPACE to clear a cell.",
        "Press ENTER to finish input.",
        "Press SPACE or click 'Solve'",
        "to solve the board."
    ]

    x_offset = 570 # Place instructions starting at 600 pixels (beside the board)
    y_offset = 25 # Start near the top of the window
    for instruction in instructions:
        text = font.render(instruction, True, BLACK)
        screen.blit(text, (x_offset, y_offset))
        y_offset += 30

# Draw the Solve button
def draw_solve_button(screen):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(BOARD_X_OFFSET, HEIGHT - 70,
                              BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)
    text = font.render("Solve", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Draw the Reset button
def draw_reset_button(screen):
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(BOARD_X_OFFSET + BUTTON_WIDTH + 10, HEIGHT - 70,
                              BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)
    text = font.render("Reset", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Allow the user to input the initial board
def user_input(screen, board):
    """
    Allow the user to input values into the Sudoku board via keyboard or mouse interaction.

    Args:
        screen (pygame.Surface): The Pygame screen on which to display the Sudoku board and interface.
        board (Board): An instance of the Board class representing the current Sudoku grid.

    The function continuously listens for user input, allowing the user to:
    - Navigate cells using the arrow keys.
    - Input numbers 1-9 to fill cells.
    - Clear cells using 0 or BACKSPACE.
    - Press ENTER to finalize input.
    - Use the mouse to click buttons such as "Solve" or "Reset".
    
    It also highlights the currently selected cell to make navigation clear.
    """

    font = pygame.font.Font(None, 36)
    current_row, current_col = 0, 0
    
    while True:
        # Draw the grid with the current board state
        draw_grid(screen, board)
        # Highlight the current cell
        pygame.draw.rect(screen, RED, 
                            (BOARD_X_OFFSET + current_col * GRID_SIZE, 
                            BOARD_Y_OFFSET + current_row * GRID_SIZE, 
                            GRID_SIZE, GRID_SIZE), 3)
        draw_instructions(screen)
        solve_button_rect = draw_solve_button(screen)
        reset_button_rect = draw_reset_button(screen)
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to finish input
                    return
                elif event.key == pygame.K_UP:
                    current_row = (current_row - 1) % 9
                elif event.key == pygame.K_DOWN:
                    current_row = (current_row + 1) % 9
                elif event.key == pygame.K_LEFT:
                    current_col = (current_col - 1) % 9
                elif event.key == pygame.K_RIGHT:
                    current_col = (current_col + 1) % 9
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    # Update the board with the number pressed
                    board.grid[current_row][current_col] = int(event.unicode)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
                    # Clear the cell
                    board.grid[current_row][current_col] = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if solve_button_rect.collidepoint(event.pos):
                        return
                    elif reset_button_rect.collidepoint(event.pos):
                        # Clear all contents from the board
                        board.grid = [[0 for _ in range(9)] for _ in range(9)]
                        draw_grid(screen, board)
                        draw_instructions(screen)
                        draw_solve_button(screen)
                        draw_reset_button(screen)
                        pygame.display.flip()


# Main function to run the Pygame loop
def main():
    """
    Initialize the Pygame environment and run the main game loop for the Sudoku player.

    This function sets up the Pygame window, creates a Board instance, allows the user to input the initial state, 
    and handles user interactions through the main event loop. It also manages the solving of the Sudoku board by 
    handling keyboard and mouse events, including:
    
    - Pressing SPACE to initiate the solving process.
    - Clicking buttons to solve or reset the board.
    - Keeping the display updated with current board and UI state.
    """
    
    # Initialize Pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Player")

    # Create a Board instance
    board = Board()

    # Allow user to input the initial state of the Sudoku board
    user_input(screen, board)

    # Draw the initial state of the board
    draw_grid(screen, board)
    draw_instructions(screen)
    solve_button_rect = draw_solve_button(screen)
    reset_button_rect = draw_reset_button(screen)
    pygame.display.flip()

    # Solver instance
    solver = Solver(board)

    # Main loop
    solving = False  # Flag to control solving process
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press spacebar to start solving
                    solving = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if solve_button_rect.collidepoint(event.pos):
                        solving = True
                    elif reset_button_rect.collidepoint(event.pos):
                        # Clear all contents from the board
                        board.grid = [[0 for _ in range(9)] for _ in range(9)]
                        draw_grid(screen, board)
                        draw_instructions(screen)
                        draw_solve_button(screen)
                        draw_reset_button(screen)
                        pygame.display.flip()

        # Solve step by step
        if solving:
            if solver.solve():
                draw_grid(screen, board)
                draw_instructions(screen)
                draw_solve_button(screen)
                draw_reset_button(screen)
                pygame.display.flip()
                solving = False  # Stop after solving
            else:
                print("No solution exists for the given Sudoku board.")
                solving = False

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
