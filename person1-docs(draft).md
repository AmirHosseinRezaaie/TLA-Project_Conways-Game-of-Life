Person = AmirHosseinRezaaie

Note: This document explains the implementation details of the Turing Machine simulator.

---

# Documents and Explanations

## Part 1 - Turing Machine Simulator

### Overview

The goal of this part is to implement a reusable deterministic Turing Machine simulator.

Implemented features:

- Generic transition function
- Configurable states
- Tape simulation
- Step-by-step execution
- Generator-based runtime
- Debug utilities
- Acceptance/Rejection APIs

---

## TuringMachine Class

**Purpose**

The `TuringMachine` class represents the whole simulator.

It stores:

- transition function
- start state
- accept state
- reject state
- blank symbol

Every Turing Machine can be created by simply passing a different transition table.

---

## Constructor (`__init__`)

**Purpose**

Initializes the machine configuration.

Stores:

- transitions
- start state
- accept state
- reject state
- blank symbol

The constructor does not execute the machine.

It only prepares the simulator.

---

## Transition Representation

Transitions are stored as a Python dictionary.

Key:

```python
(current_state, current_symbol)
```

Value:

```python
(next_state, write_symbol, direction)
```

Example:

```python
('q0', '#') -> ('q1', '#', 'R')
```

Dictionary lookup provides constant-time access to transition rules.

---

## Tape Representation

The tape is represented using three components:

- `left_hand_side`
- `symbol`
- `right_hand_side`

Current machine configuration is stored inside:

```python
configuration
```

Each configuration also stores the current state.

This representation makes head movement simple and efficient.

---

## Blank Symbol

The simulator uses

```python
blank_symbol = ''
```

to represent empty tape cells.

Whenever the head moves beyond initialized cells, the blank symbol is used automatically.

---

## Execution Engine (`run()`)

The `run()` method performs the simulation.

Main responsibilities:

- initialize tape
- initialize configuration
- execute transitions
- update tape
- move head
- detect accept state
- detect reject state
- yield every configuration

The method is implemented as a Python Generator.

---

## Generator Design

Instead of returning only the final result,

`run()` yields every machine configuration.

Advantages:

- step-by-step execution
- debugging support
- lower memory usage
- interactive simulation

---

## Head Movement

Two directions are supported:

- `R`
- `L`

Moving right:

- push current symbol to left tape
- read first symbol from right tape

Moving left:

- push current symbol to right tape
- restore last symbol from left tape

Crossing the left boundary generates a warning.

---

## Accept / Reject Detection

Execution stops when:

- accept state is reached
- reject state is reached
- transition does not exist

Missing transitions are treated as rejection.

---

## accepts()

Returns:

- `True`
- `False`
- `None`

`None` means the machine did not halt before reaching the step limit.

The method internally uses `run()`.

---

## rejects()

Wrapper around `accepts()`.

Simply returns the logical opposite result.

No duplicated simulation is performed.

---

## debug()

Prints every machine configuration.

Output format:

```
state: left[symbol]right
```

Useful for:

- debugging
- tracing execution
- testing transition tables

---

## Error Handling

Implemented checks:

- empty input
- missing transition
- invalid direction
- step limit warning
- left boundary warning

Python logging is used for warnings.

---

## Design Decisions

### Why Dictionary?

Fast transition lookup.

---

### Why Generator?

Supports incremental execution.

---

### Why deepcopy()?

Each yielded configuration remains immutable.

Future updates do not modify previous states.

---

### Why step_limit?

Prevents infinite loops during testing.

---

## Result

The simulator is completely generic.

Different Turing Machines can be executed without modifying the simulator.

Only the transition table needs to change.