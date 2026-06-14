# -*- coding: utf-8 -*-
"""A Turing machine simulator skeleton.

    Accepting '#'
    =============

    >>> from turing_machine import TuringMachine

    Instantiate the machine with particular transitions.

    >>> one_hash = TuringMachine(
    ...     {
    ...         ('q0', '#'): ('saw_#', '#', 'R'),
    ...         ('saw_#', ''): ('qa', '', 'R'),
    ...     }
    ... )

    Check whether it accepts a string:

    >>> one_hash.accepts('#')
    True

    >>> one_hash.accepts('##')
    False

    Check whether it rejects a string:

    >>> one_hash.rejects('#')
    False

    >>> one_hash.rejects('##')
    True

"""

import logging
from itertools import islice
import copy


class TuringMachine:
    """Turing machine simulator class.

    A machine is instantiated with transitions, start, accept and reject states
    and a blank symbol. We assume that the input and the tape alphabet can be
    deducted from the transitions.

    :param dict transitions: a mapping from (state, symbol) tuples to (state,
    symbol, direction) tuple. Directions are either 'L' (for left) or 'R' (for right).

    :param start_state: the initial state of the machine.

    :param accept_state: the accept state.

    :param reject_state: the reject state.

    :blank_symbol: the special symbol that marks the tape cell to be empty.

    """

    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=''):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

    def run(self, input_):
        """Execute the Turing machine for a particular input.

        :param input_: the input that is written on the tape. It can be a list
        of strings, or just a string, in which case each letter is treated as a symbol.

        This method MUST be a Python generator. It should yield a (action, configuration) tuple
        at each step of the computation.
        
        The action is either 'Accept', 'Reject' or None. 
        
        Configuration is a dictionary with the following keys:
        - 'state': the current state,
        - 'left_hand_side': list of symbols on the left hand side of the current position (closest first),
        - 'symbol': the current symbol under the head,
        - 'right_hand_side': list of symbols on the right hand side of the current position.

        """

        # =-=-=-= Init Cofiguration: (Tape config) =-=-=-=
        # Eror handling for Empty input:
        current_symbol = (
            input_[0]
            if len(input_) > 0
            else self.blank_symbol
        )

        configuration = {
            "state": self.start_state,
            "left_hand_side": [],
            "symbol": current_symbol,
            "right_hand_side": list(input_[1:])
        }
        
        yield None, copy.deepcopy(configuration)

        while(True):

            # if Accept: return
            if configuration["state"] == self.accept_state:
                yield "Accept", copy.deepcopy(configuration)
                return
            # if Reject: return
            if configuration["state"] == self.reject_state:
                yield "Reject", copy.deepcopy(configuration)
                return

            #  Find Transition in Transitions:
            if ((configuration["state"], configuration["symbol"]) in self.transitions):
                # Extract Transition component:
                next_state , write_symbol, direction = self.transitions[(configuration["state"], configuration["symbol"])]
                
                # Update Config:
                configuration["symbol"] = write_symbol
                configuration["state"] = next_state

                # Move: Right
                if(direction == "R"):
                    # Push current cell to the left side of the tape:
                    configuration["left_hand_side"].insert(
                        0,
                        configuration["symbol"]
                    )

                    # Move to right:
                    if configuration["right_hand_side"]:
                        configuration["symbol"] = configuration["right_hand_side"].pop(0)
                    # Empty right:
                    else:
                        configuration["symbol"] = self.blank_symbol

                # Move Left:
                elif direction == "L":
                    # Push Current cell to the right side of the tape:
                    configuration["right_hand_side"].insert(
                        0,
                        configuration["symbol"]
                    )

                    # Move to left:
                    if configuration["left_hand_side"]:
                        configuration["symbol"] = configuration["left_hand_side"].pop(0)
                    # Empty left:
                    else:
                        # in Todo: Log a warning using logging.warning()
                        logging.warning(
                            "Crossed the left boundary of singly-infinite tape."
                        )
                        configuration["symbol"] = self.blank_symbol

                # if  invalid Transition:
                else:
                    raise ValueError(
                        f"Unknown direction: {direction}"
                    )

                yield None, copy.deepcopy(configuration)
                    
            
            else:
                yield "Reject", copy.deepcopy(configuration)
                return



        


    def accepts(self, input_, step_limit=100):
        """Check whether the Turing machine accepts a string.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to simulate before stopping.
        :return: True if the machine halts in accept_state, False if it rejects,
                 or None if the step limit is reached without halting.
        """

        # Run(input):
        Outputs = self.run(input_)

        # Check outputs:
        # Use islice to consume at most step_limit configurations from the generator.
        for action, config in islice(Outputs, step_limit):

            if(action == "Accept"):
                return True
            elif(action == "Reject"):
                return False
            
        # if no Halting:
        logging.warning(
            "Step-limit is reached without Halting"
        )
        return None

    def rejects(self, input_, **kwargs):
        """Check whether the Turing machine rejects a string.

        :param input_: the input string or list.
        :return: True if the machine rejects the string, False if it accepts.
        """
        
        if(self.accepts(input_, **kwargs) is None):
            return None
        
        else:
            return not self.accepts(input_, **kwargs)

    def debug(self, input_, step_limit=100, colored=False):
        """Print the execution configuration of the machine per transition for debugging.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to output.
        :param colored: True to output colored boundaries in terminal.
        """
        Outputs = self.run(input_)

        for action, config in islice(Outputs, step_limit):
            # Left side -> Reverse 
            left = ''.join(reversed(config["left_hand_side"]))
            # Right side -> Same
            right = ''.join(config["right_hand_side"])

            print(
                f'{config["state"]}: {left}[{config["symbol"]}]{right}'
            )
