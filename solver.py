"""
solver.py

This module provides the core logic for solving a Sudoku puzzle. It contains the `Board` class for managing
the Sudoku grid and the `Solver` class for implementing the logic to solve the puzzle.

Classes:
    - Board: Represents the Sudoku board with methods to manage its state.
    - Solver: Implements the backtracking algorithm to solve the given Sudoku board, checking validity
      and attempting to place numbers according to Sudoku rules.

The `Solver` class uses the `Board` instance to manage the puzzle state and attempts to solve it by
trying different numbers while ensuring each placement follows Sudoku rules.
"""

import math

class Board:
    
    def __init__(self):
        # Initialize the board as an empty grid
        self.grid = [[0 for _ in range(9)] for _ in range(9)]


    def initial_state(self):
        # Set the initial state of the board
        initial_board = [
            [0, 0, 0, 0, 0, 0, 0, 1, 8],
            [0, 5, 7, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 6, 2],
            [7, 0, 0, 0, 0, 9, 1, 0, 5],
            [0, 0, 0, 0, 6, 0, 0, 7, 0],
            [0, 0, 2, 0, 0, 0, 0, 3, 0],
            [8, 0, 1, 0, 0, 7, 0, 0, 0],
            [0, 0, 9, 6, 0, 0, 0, 2, 0],
        ]
        self.grid = initial_board
    

class Solver:
    def __init__(self, board):
        # Store a reference to the Board instance
        self.board = board


    def is_valid(self, cell, number):
        """
        Check if a number can be placed in a specific cell of the Sudoku board.
        
        Args:
            cell (tuple): A tuple (i,j) where 'i' is the row index and 'j' is the column index.
            number (int): The number to be placed in the cell (must be between 1-9).

        Returns:
            bool: True if the number can be placed in the specified cell without violating Sudoku rules,
            otherwise False.

        Raises:
            ValueError: If the provided cell indices or number are out of valid range.
        """

        # Unpack cell
        i, j = cell

        # Validate the cell
        if i < 0 or i >= len(self.board.grid) or j < 0 or j >= len(self.board.grid [i]):
            raise ValueError(f"Invalid action: {cell} is out of bounds.")
        if self.board.grid[i][j] != 0:
            raise ValueError(f"Invalid action: Cell {cell} is already occupied.")

        # Check row for the presence of the number
        if number in self.board.grid[i]:
            return False

        # Check column for the presence of the number
        column_values = [self.board.grid[row][j] for row in range(9)]
        if number in column_values:
            return False

        # Determine the Starting Point of the Subgrid
        subgrid_row_start = (i // 3) * 3
        subgrid_col_start = (j // 3) * 3

        # Check 3x3 Subgrid for presence of number
        for row in range(subgrid_row_start, subgrid_row_start+3):
            for col in range(subgrid_col_start, subgrid_col_start+3):
                if self.board.grid[row][col] == number:
                    return False
        
        # If all checks pass, the number is valid
        return True

    def solve(self):
        """
        Solve the Sudoku puzzle using a backtracking algorithm.

        This method attempts to fill each empty cell in the Sudoku grid with a number between 1 and 9.
        It uses a recursive backtracking approach to explore possible solutions and find a valid
        configuration for the entire board.

        Returns:
            bool: True if the board is successfully solved, False if no solution exists.
        """
                
        # Loop through every cell in the grid to find the first empty cell (value == 0)
        for row in range(0, len(self.board.grid)):
            for col in range(0, len(self.board.grid[row])):
                    if self.board.grid[row][col] == 0:
                        # Try placing numbers 1-9 in the empty cell
                        for number in range(1, 10):
                            # Check if placing this number is valid
                            if self.is_valid((row, col), number):
                                # Place the number in the cell
                                self.board.grid[row][col] = number

                                # Recursively call solve to continue
                                if self.solve():
                                    return True
                                
                                # If solve() did not succeed, backtrack and reset the cell
                                self.board.grid[row][col] = 0

                        # If no number from 1-9 works, return False to signal backtracking
                        return False
                    
        # If all cells are filled correctly, return True (meaning the board is solved)
        return True


if __name__ == "__main__":
    # Create Board and Solver Instances
    board = Board()
    board.initial_state()  # Sets the initial state

    solver = Solver(board)  # Create solver and pass the board

    # Call the solve method
    if solver.solve():
        # Print the solved Sudoku board
        for row in solver.board.grid:
            print(row)
    else:
        print("No solution exists for the given Sudoku board.")