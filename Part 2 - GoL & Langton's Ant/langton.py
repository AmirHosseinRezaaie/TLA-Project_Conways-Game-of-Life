# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""
import numpy as np


class LangtonsAnt:
    """
    TODO: [Part 2 - Langton's Ant]
    Create the LangtonsAnt class.
    
    Instruct students to:
    1. Implement the core rules:
       - If on a white square, toggle the color of the square and turn 90 degrees clockwise ('R'), then move forward one unit.
       - If on a black square, toggle the color of the square and turn 90 degrees counter-clockwise ('L'), then move forward one unit.
    2. Extend it to handle multi-color states (representing rulesets like RLR, LLRR, LRRRRRLLR, etc.).
       - A ruleset dictionary maps: {current_color: (next_color, turn_direction)}
       - Where turn_direction is 'R' or 'L'.
    3. Ensure wrapping at the boundaries (toroidal grid).
    """

    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.
        
        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): Dictionary defining transition rules.
                          Format: {current_color: (next_color, turn_direction)}
        """
        self.N = N
        self.grid = np.zeros((N, N), dtype=int)
        self.ant_pos = list(ant_position)
        self.rules = rules
        self.direction = 0  # 0: North, 1: East, 2: South, 3: West

    def get_states(self):
        """
        Returns the current state grid of the cells.
        
        Returns:
            np.ndarray: The NxN cellular grid.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).
        
        Returns:
            tuple: Current coordinates of the ant.
        """
        return tuple(self.ant_pos)

    def step(self):
        """
        Perform a single simulation step following the ruleset.
        """
        r, c = self.ant_pos
        current_color = self.grid[r, c]
        
        if current_color not in self.rules:
            return
            
        next_color, turn_dir = self.rules[current_color]
        
        self.grid[r, c] = next_color
        
        if turn_dir == 'R':
            self.direction = (self.direction + 1) % 4
        elif turn_dir == 'L':
            self.direction = (self.direction - 1) % 4
            
        if self.direction == 0:
            r -= 1
        elif self.direction == 1:
            c += 1
        elif self.direction == 2:
            r += 1
        elif self.direction == 3:
            c -= 1
            
        self.ant_pos = [r % self.N, c % self.N]

    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()
