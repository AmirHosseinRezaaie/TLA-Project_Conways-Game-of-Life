# -*- coding: utf-8 -*-
"""
tla_lab.core.busy_beaver
==========================

Wraps the original ``Part 1 - Busy Beaver/busy_beaver.py`` (its own small
``TuringMachine`` class and the ``beaver_programs`` table for n = 1..5) and
adds two things the brief asks for:

1. :func:`run_beaver` - runs one of the *existing* ``beaver_programs``
   machines and returns a structured result (steps, ones written, halted or
   not) instead of only printing to stdout, so a GUI can display it.

2. :class:`BusyBeaverSearch` - an *opt-in*, bounded brute-force search over
   2-symbol Turing machines for a given number of states. This is a genuine
   enumerate-and-simulate search (not a lookup table), but it is capped by
   both a step limit *and* a wall-clock timeout, and it can be cancelled,
   exactly as section 6 of the brief requires. It is only practical for a
   small number of states (2, and 3 with a modest timeout); the module makes
   no claim about finding *the* proven Busy Beaver champion for a given
   n - it reports whatever the best machine found during the (bounded)
   search actually did, nothing more.

No new "known best" numbers are hard-coded anywhere in this file. Anything
shown to the user is either (a) taken from the project's own
``beaver_programs`` table and re-run live, or (b) the actual result of a
search that ran in this process.
"""

from __future__ import annotations

import itertools
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from tla_lab.utils.paths import ensure_legacy_paths_importable

ensure_legacy_paths_importable()

# Original, unmodified implementation (its own tiny TuringMachine + table).
import busy_beaver as _legacy  # noqa: E402

Program = Dict[str, Tuple[str, str, str]]


@dataclass
class BeaverResult:
    states: int
    halted: bool
    steps: int
    ones_written: int
    tape: str
    program: Program


def available_state_counts() -> List[int]:
    """States for which the project already ships a hand-written machine
    (index 0 is an intentionally empty placeholder in the original list)."""
    return [n for n in range(1, len(_legacy.beaver_programs)) if _legacy.beaver_programs[n]]


def run_beaver(n: int, step_limit: int = 200_000) -> BeaverResult:
    """Run the *existing* beaver_programs[n] machine (unchanged logic from
    Part 1) and return a structured result instead of printing.

    :raises ValueError: if ``n`` has no program defined in the original
        table, or is out of range.
    """
    if n <= 0 or n >= len(_legacy.beaver_programs) or not _legacy.beaver_programs[n]:
        raise ValueError(f"No Busy Beaver program is defined for n={n} in this project.")

    program = _legacy.beaver_programs[n]
    tm = _legacy.TuringMachine(program, "a", "h", "0")

    steps = 0
    halted = False
    # Re-implements the original run() loop with a step_limit so a
    # non-halting/misconfigured program can never hang the GUI.
    while tm.state != tm.halt and steps < step_limit:
        lhs = tm.get_lhs()
        rhs = tm.get_rhs(lhs)
        new_state, new_symbol, move = rhs
        old_symbol = lhs[1]
        tm.update_tape(old_symbol, new_symbol)
        tm.update_state(new_state)
        tm.move_head(move)
        steps += 1

    halted = tm.state == tm.halt
    tape_str = "".join(tm.tape)
    ones = tape_str.count("1")
    return BeaverResult(
        states=n, halted=halted, steps=steps, ones_written=ones,
        tape=tape_str, program=program,
    )


# ---------------------------------------------------------------------------
# Bounded brute-force search engine (opt-in, Priority 3 feature)
# ---------------------------------------------------------------------------

_SYMBOLS = ("0", "1")
# NOTE: the project's own busy_beaver.TuringMachine.move_head() only
# understands lowercase 'l' / 'r' (see Part 1 - Busy Beaver/busy_beaver.py),
# unlike the Part 1 turing_machine.py module which uses 'L' / 'R'. The search
# engine must speak whichever dialect the engine it drives actually expects.
_DIRECTIONS = ("l", "r")


def _enumerate_programs(n_states: int):
    """Yield every 2-symbol, n-state transition table as a dict of
    ``{state+symbol: (state, symbol, direction)}``, plus an explicit halt
    transition. This is the classic Busy Beaver enumeration; the number of
    machines grows as ``(4(n+1))^(2n)``, which is why this is only offered
    for small ``n`` with a timeout.
    """
    states = [chr(ord("a") + i) for i in range(n_states)]
    halt_state = "h"
    targets = states + [halt_state]

    # one (state, symbol, direction) choice per (state, read-symbol) cell
    cell_choices = list(itertools.product(targets, _SYMBOLS, _DIRECTIONS))
    keys = [s + sym for s in states for sym in _SYMBOLS]

    for combo in itertools.product(cell_choices, repeat=len(keys)):
        yield dict(zip(keys, combo))


@dataclass
class SearchProgress:
    n_states: int
    machines_tried: int = 0
    best_ones: int = -1
    best_steps: int = 0
    best_program: Optional[Program] = None
    cancelled: bool = False
    timed_out: bool = False
    elapsed_seconds: float = 0.0


class BusyBeaverSearch:
    """Bounded brute-force Busy Beaver search for small state counts.

    Usage::

        search = BusyBeaverSearch(n_states=2, step_limit=200, timeout_s=5)
        progress = search.run(on_progress=lambda p: print(p.machines_tried))

    ``run`` can be interrupted at any time with :meth:`cancel` (e.g. from a
    GUI "Stop" button running on another thread) and always stops on its
    own after ``timeout_s`` seconds, so it can never freeze the caller.
    """

    def __init__(self, n_states: int, step_limit: int = 200, timeout_s: float = 5.0):
        if n_states < 1:
            raise ValueError("n_states must be >= 1")
        self.n_states = n_states
        self.step_limit = step_limit
        self.timeout_s = timeout_s
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def _simulate(self, program: Program) -> Tuple[bool, int, int]:
        """Run one candidate program with the project's own TuringMachine
        engine. Returns (halted, steps, ones_written)."""
        tm = _legacy.TuringMachine(program, "a" if self.n_states else "a", "h", "0")
        steps = 0
        while tm.state != "h" and steps < self.step_limit:
            key = tm.state + tm.tape[tm.pos]
            if key not in program:
                return False, steps, "".join(tm.tape).count("1")
            new_state, new_symbol, move = program[key]
            old_symbol = tm.tape[tm.pos]
            tm.update_tape(old_symbol, new_symbol)
            tm.update_state(new_state)
            tm.move_head(move)
            steps += 1
        halted = tm.state == "h"
        return halted, steps, "".join(tm.tape).count("1")

    def run(self, on_progress=None, progress_every: int = 500) -> SearchProgress:
        progress = SearchProgress(n_states=self.n_states)
        start = time.monotonic()

        for program in _enumerate_programs(self.n_states):
            if self._cancelled:
                progress.cancelled = True
                break
            if time.monotonic() - start > self.timeout_s:
                progress.timed_out = True
                break

            halted, steps, ones = self._simulate(program)
            progress.machines_tried += 1

            if halted and ones > progress.best_ones:
                progress.best_ones = ones
                progress.best_steps = steps
                progress.best_program = program

            if on_progress and progress.machines_tried % progress_every == 0:
                progress.elapsed_seconds = time.monotonic() - start
                on_progress(progress)

        progress.elapsed_seconds = time.monotonic() - start
        return progress


__all__ = [
    "BeaverResult", "run_beaver", "available_state_counts",
    "BusyBeaverSearch", "SearchProgress",
]
