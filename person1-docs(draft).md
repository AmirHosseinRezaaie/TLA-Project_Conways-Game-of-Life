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

## Example 1 Analysis

**Purpose**

This example accepts only the input `##`.

### States

| State | Purpose |
|-------|---------|
| `q0` | Initial state |
| `saw_#` | First `#` has been read |
| `saw_##` | Second `#` has been read |
| `qa` | Accept state |

### Behavior

Accepted input:

```text
##
```

Rejected examples:

```text
#
###
######
101031##
#_#_
```

The machine checks that the tape contains exactly two `#` symbols and nothing else. Any additional or missing symbol causes the machine to reject the input.

---

## Example 2 Analysis

**Purpose**

This example verifies that the strings before and after the `#` delimiter are identical.

### States

| State | Purpose |
|-------|---------|
| `q0` | Initial state |
| `FindDelimiter0` | Search for the delimiter after reading `0` |
| `FindDelimiter1` | Search for the delimiter after reading `1` |
| `Check0` | Verify a matching `0` |
| `Check1` | Verify a matching `1` |
| `FindLeftmost` | Return to the beginning of the tape |
| `FindNext` | Find the next unchecked symbol |
| `End` | Verify that all symbols have been processed |
| `qa` | Accept state |

### Behavior

Accepted examples:

```text
#
0#XXXX0
1#XXXX1
11#XXXX11
01#01
101#101
```

Rejected examples:

```text
0000#XXXX1
0111#XXXX1
0111#XXXX0
11#XXXX1
```

During execution, every matched symbol is replaced with `X`. The machine accepts only when every symbol before the delimiter has a matching symbol after the delimiter and the entire input has been successfully processed.

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

---

# Testing

The simulator was tested using the provided examples and the self-check script.

## Example Test 1

A simple machine that accepts only the string:

```
##
```

Results:

- `##` → Accepted
- `101031##` → Rejected
- `######` → Rejected
- `#####` → Rejected
- `#_#_` → Rejected

The execution trace produced by `debug()` matched the expected state transitions.

---

## Example Test 2

A more complex transition table was tested.

This machine compares symbols around the `#` delimiter and replaces matched symbols with `X`.

Verified examples:

- `#` → Accepted
- `0#XXXX0` → Accepted
- `1#XXXX1` → Accepted
- `11#XXXX11` → Accepted
- `01#XXXX01` → Accepted
- `01#01` → Accepted
- `101#101` → Accepted

Rejected examples:

- `0000#XXXX1`
- `0111#XXXX1`
- `0111#XXXX0`
- `11#XXXX1`

The final tape contents also matched the expected results (e.g. `XX#XX` and `XXX#XXX`).

---

## Student Self-Test

The implementation successfully passed all provided self-check tests.

Verified features:

- successful module import
- accept/reject interface
- generator-based execution
- configuration dictionary format
- tape boundary handling

The simulator completed every test without runtime errors.

---

## Overall Result

All provided tests passed successfully.

The simulator correctly executes deterministic Turing Machines, follows the supplied transition table, updates the tape correctly, and provides step-by-step execution through the generator interface.

---

## Unary Addition Turing Machine

### Unary Representation

In this project, non-negative integers are represented using unary notation. Each number is encoded as a sequence of `1` symbols, while the separator between the two operands is represented by the symbol `0`.

Examples:

| Arithmetic Expression | Unary Input |
|----------------------|-------------|
| 2 + 3 | `110111` |
| 3 + 4 | `11101111` |
| 0 + 3 | `0111` |

The blank symbol is represented by the empty string (`''`).

---

### Addition Algorithm

The unary addition machine follows a simple strategy:

1. Start from the beginning of the tape.
2. Move the head to the right until the separator (`0`) is found.
3. Remove the separator by replacing it with the blank symbol.
4. Move the head back toward the beginning of the tape.
5. Halt in the accept state.

Since removing the separator concatenates the two unary numbers, the resulting tape directly represents the sum of the two operands.

---

### Machine States

| State | Purpose |
|--------|---------|
| `q0` | Scan the first operand until the separator is reached. |
| `q_back` | Return the tape head to the beginning of the tape. |
| `qa` | Accept state. |

---

### Example Execution

Input:

```
110111
```

Initial tape:

```
11 0 111
```

After removing the separator:

```
11111
```

Final tape:

```
11111
```

which corresponds to:

```
2 + 3 = 5
```

---

### Test Cases

| Input | Arithmetic | Output Tape | Result |
|------|------------|-------------|--------|
| `110111` | 2 + 3 | `11111` | Accepted |
| `11101111` | 3 + 4 | `1111111` | Accepted |
| `0111` | 0 + 3 | `111` | Accepted |

---

### Discussion

After removing the separator, the simulator moves the tape head back to the beginning before entering the accept state. This behavior prepares the tape for possible subsequent computations.

During execution on the current singly-infinite tape implementation, moving left beyond the initial tape boundary produces a warning. This behavior is expected according to the project specification and will be eliminated after implementing the two-way infinite tape extension in the next phase.