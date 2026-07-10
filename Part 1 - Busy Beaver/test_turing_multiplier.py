# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

transitions = {

    # Select next symbol
    ('q0', '1'): ('q1', 'A', 'R'),
    ('q0', '0'): ('q7', '0', 'L'),

    # Move to separator
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '0'): ('q2', '0', 'R'),

    # Mark multiplier
    ('q2', '1'): ('q2', 'B', 'R'),
    ('q2', ''): ('q3', '', 'L'),
    ('q2', 'C'): ('q3', 'C', 'L'),

    # Return one mark
    ('q3', 'B'): ('q4', '1', 'R'),

    # Append result
    ('q4', 'C'): ('q4', 'C', 'R'),
    ('q4', '1'): ('q4', '1', 'R'),
    ('q4', ''): ('q5', 'C', 'L'),

    # Continue copying
    ('q5', 'B'): ('q4', '1', 'R'),
    ('q5', 'C'): ('q5', 'C', 'L'),
    ('q5', '1'): ('q5', '1', 'L'),
    ('q5', '0'): ('q6', '0', 'L'),

    # Back to left side
    ('q6', '1'): ('q6', '1', 'L'),
    ('q6', 'A'): ('q0', 'A', 'R'),

    # Finish work
    ('q7', 'A'): ('q7', 'A', 'L'),
    ('q7', ''): ('q8', '', 'R'),

    # Clean tape
    ('q8', '1'): ('q8', '', 'R'),
    ('q8', 'C'): ('q8', '1', 'R'),
    ('q8', 'A'): ('q8', '', 'R'),
    ('q8', 'B'): ('q8', '', 'R'),
    ('q8', '0'): ('q8', '', 'R'),

    # Accept
    ('q8', ''): ('qa', '', 'R')

}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(
        transitions,
        start_state='q0',
        accept_state='qa'
    )

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=1000)

        print("-" * 20)

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111 

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111 

    run("01111")
    # outputs []