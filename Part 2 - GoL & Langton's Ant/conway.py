"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath):
    live_cells = []
    width = 0
    height = 0
    
    with open(filepath, 'r') as file:
        lines = file.readlines()
        
    if filepath.endswith('.cells'):
        row_idx = 0
        for line in lines:
            line = line.strip()
            if line.startswith('!') or len(line) == 0:
                continue
            
            if len(line) > width:
                width = len(line)
                
            col_idx = 0
            for char in line:
                if char == 'O' or char == 'o':
                    live_cells.append((row_idx, col_idx))
                col_idx += 1
            row_idx += 1
        height = row_idx
        
    elif filepath.endswith('.rle'):
        row_idx = 0
        col_idx = 0
        pattern_data = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                continue
            if line.startswith('x'):
                parts = line.split(',')
                width_part = parts[0].split('=')[1]
                width = int(width_part.strip())
                height_part = parts[1].split('=')[1]
                height = int(height_part.strip())
                continue
            pattern_data += line
            
        count_str = ""
        for char in pattern_data:
            if char.isdigit():
                count_str += char
            elif char == 'b':
                num = 1
                if len(count_str) > 0:
                    num = int(count_str)
                col_idx += num
                count_str = ""
            elif char == 'o':
                num = 1
                if len(count_str) > 0:
                    num = int(count_str)
                for _ in range(num):
                    live_cells.append((row_idx, col_idx))
                    col_idx += 1
                count_str = ""
            elif char == '$':
                num = 1
                if len(count_str) > 0:
                    num = int(count_str)
                row_idx += num
                col_idx = 0
                count_str = ""
            elif char == '!':
                break
                
    return width, height, live_cells
class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=False):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0  # do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # use for slow implementation of evolve
        self.cols = N  # use for slow implementation of evolve

    def getStates(self):
        """
        Returns the current states of the cells
        """
        return self.grid

    def getGrid(self):
        """
        Same as getStates()
        """
        return self.getStates()

    def update_grid_fast(self, grid):
        """
        TODO: [Part 1e - Fast Convolution]
        Use scipy.signal.convolve2d (or similar) to compute neighbor weights
        rapidly for large grids (N > 1024).
        
        Args:
            grid (np.ndarray): The current 2D grid of states.
            
        Returns:
            np.ndarray: The next 2D grid of states.
        """
        # Student TODO: Implement fast 2D convolution method
        return grid

    def evolve(self):
        """
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        """
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            next_grid = np.zeros((self.rows, self.cols), dtype=np.uint)
            for r in range(self.rows):
                for c in range(self.cols):
                    live_neighbors = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr = r + dr
                            nc = c + dc
                            if self.finite:
                                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                    if self.grid[nr, nc] == 1:
                                        live_neighbors += 1
                            else:
                                nr = nr % self.rows
                                nc = nc % self.cols
                                if self.grid[nr, nc] == 1:
                                    live_neighbors += 1
                    if self.grid[r, c] == 1:
                        if live_neighbors == 2 or live_neighbors == 3:
                            next_grid[r, c] = 1
                    else:
                        if live_neighbors == 3:
                            next_grid[r, c] = 1
            self.grid = next_grid

    def insertBlinker(self, index=(0, 0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        '''
        TODO: [Part 1c - Glider Gun Fix]
        The current glider gun pattern is broken. Leave the broken array in the code 
        and instruct the student to debug and fix the coordinates so it loops infinitely.
        '''
        self.grid[index[0] + 1, index[1] + 25] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 25] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 21] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 35] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 21] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 35] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 11] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 21] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 11] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 25] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 11] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 25] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue

    def insertFromFile(self, filename, index=((0, 0))):
        '''
        Insert cells from pattern file using parse_pattern
        '''
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue
