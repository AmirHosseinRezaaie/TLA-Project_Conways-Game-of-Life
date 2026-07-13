# -*- coding: utf-8 -*-

from logic_gates import GliderLogicGates
from pygame_viewer import run_pygame_life
import time

def demo_and_gate():
    gates = GliderLogicGates()
    print("\n=== Demonstrating AND Gate ===")
    
    combinations = [
        (False, False, "False (Empty)"),
        (False, True,  "False (Passes through)"),
        (True,  False, "False (Passes through)"),
        (True,  True,  "True (Block formed)")
    ]
    
    for a, b, outcome in combinations:
        print(f"Showing AND Gate: Input A={a}, Input B={b}")
        gol = gates.setup_and_gate(grid_size=35, input_a_present=a, input_b_present=b)
        title = f"AND Gate | A={a}, B={b} | Output: {outcome}"
        run_pygame_life(gol, cell_scale=15, fps=10, max_frames=35, title=title)
        time.sleep(0.5)


def demo_not_gate():
    gates = GliderLogicGates()
    print("\n=== Demonstrating NOT Gate ===")
    
    combinations = [
        (False, "True (Signal Survives)"),
        (True,  "False (Signal Destroyed)")
    ]
    
    for a, outcome in combinations:
        print(f"Showing NOT Gate: Input A={a}")
        gol = gates.setup_not_gate(grid_size=35, input_a_present=a)
        title = f"NOT Gate | A={a} | Output: {outcome}"
        run_pygame_life(gol, cell_scale=15, fps=10, max_frames=35, title=title)
        time.sleep(0.5)


if __name__ == '__main__':
    print("Launching all 6 visual logic gate demonstrations sequentially.")
    print("Each window will automatically close and advance after a few seconds.")
    demo_and_gate()
    demo_not_gate()
    print("All demonstrations complete!")
