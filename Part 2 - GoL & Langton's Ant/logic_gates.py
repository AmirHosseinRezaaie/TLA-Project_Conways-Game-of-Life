# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Student Template Module.

"""
# pyrefly: ignore [missing-import]
import numpy as np
from conway import GameOfLife


class GliderLogicGates:
    """
    TODO: [Extension - Logic Gates]
    Instruct the student to:
    1. Initialize a grid and precisely place "Glider" streams (signals represented by gliders)
       such that their collision simulates:
       - An AND gate (produces a specific output pattern only when both inputs A and B are active).
       - A NOT gate (produces an output signal/glider only when input A is inactive).
    2. Prove the Turing completeness of Conway's Game of Life by demonstrating these logic gates.
    """

    def setup_and_gate(self, grid_size=35, input_a_present=False, input_b_present=False):
        """
        Set up the Game of Life grid for an AND gate.
        
        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            input_b_present (bool): If True, place glider for Input B.
            
        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        gol = GameOfLife(N=grid_size)
        
        if input_a_present:
            # Shifted from (2, 2) to (9, 6) so it crashes at (15, 12)
            gol.insertGlider(index=(9, 6))
            
        if input_b_present:
            # Shifted from (2, 14) to (9, 18) so it crashes at (15, 12)
            r = 9
            c = 18
            gol.grid[r, c+1] = gol.aliveValue
            gol.grid[r+1, c] = gol.aliveValue
            gol.grid[r+2, c] = gol.aliveValue
            gol.grid[r+2, c+1] = gol.aliveValue
            gol.grid[r+2, c+2] = gol.aliveValue
            
        return gol

    def setup_not_gate(self, grid_size=35, input_a_present=False):
        """
        Set up the Game of Life grid for a NOT gate.
        
        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            
        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        gol = GameOfLife(N=grid_size)
        
        # The "Power Supply" or "Control Glider": Always fired from (9, 6)
        # This represents our default output of True (1)
        gol.insertGlider(index=(9, 6))
        
        # Input A: If present, it fires from (9, 18) to crash into the Control Glider
        if input_a_present:
            r, c = 9, 18
            gol.grid[r, c+1] = gol.aliveValue
            gol.grid[r+1, c] = gol.aliveValue
            gol.grid[r+2, c] = gol.aliveValue
            gol.grid[r+2, c+1] = gol.aliveValue
            gol.grid[r+2, c+2] = gol.aliveValue
        return gol

    def run_and_gate(self, input_a_present, input_b_present):
        """
        Run the AND gate simulation for a specific number of steps and return the output.
        
        Args:
            input_a_present (bool): Input A state.
            input_b_present (bool): Input B state.
            
        Returns:
            bool: True if output is active (e.g. glider/block formed in output region), False otherwise.
        """
        gol = self.setup_and_gate(grid_size=35, input_a_present=input_a_present, input_b_present=input_b_present)
        
        # Advance the simulation 30 generations to allow gliders to collide
        for _ in range(30):
            gol.tick()
            
        # We MUST evaluate the target coordinate!
        # If both gliders hit and form a Block, the Block will be stationary and remain at (15, 12).
        # If only one glider was fired, it will fly straight through (15, 12) and by Step 30, 
        # it will have already moved far past it, leaving (15, 12) completely empty!
        
        # Check if there is any living cell exactly at or immediately adjacent to the target (15, 12)
        target_area = gol.grid[14:17, 11:14]
        
        if np.sum(target_area) > 0:
            return True
            
        return False

    def run_not_gate(self, input_a_present):
        """
        Run the NOT gate simulation for a specific number of steps and return the output.
        
        Args:
            input_a_present (bool): Input A state.
            
        Returns:
            bool: True if output is active, False otherwise.
        """
        gol = self.setup_not_gate(grid_size=35, input_a_present=input_a_present)
        
        # Advance the simulation 30 generations
        for _ in range(30):
            gol.tick()
            
        # If the Control Glider survived (Input A was False), it will still be a glider (5 cells)
        # If Input A was True, they crash and form a Block (4 cells)
        total_cells = np.sum(gol.grid)
        
        # The NOT gate should only return True if the single Control Glider survived!
        if total_cells == 5:
            return True
            
        return False


if __name__ == '__main__':
    gates = GliderLogicGates()
    
    print("--- Demonstrating AND Gate ---")
    print("Input A | Input B | Output")
    print("-" * 26)
    
    # Test all 4 combinations (The Truth Table)
    for a in [False, True]:
        for b in [False, True]:
            result = gates.run_and_gate(input_a_present=a, input_b_present=b)
            print(f"  {str(a):<5} |  {str(b):<5}  |  {str(result)}")
            
    print("\n--- Demonstrating NOT Gate ---")
    print("Input A | Output")
    print("-" * 18)
    
    # Test both combinations
    for a in [False, True]:
        result = gates.run_not_gate(input_a_present=a)
        print(f"  {str(a):<5} |  {str(result)}")
