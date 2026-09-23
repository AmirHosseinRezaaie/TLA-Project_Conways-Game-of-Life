# -*- coding: utf-8 -*-
"""
tla_lab.core.langtons_ant
============================

Wraps the original ``Part 2 - GoL & Langton's Ant/langton.py``
(``LangtonsAnt`` class - toroidal grid, direction handling, the classic
"toggle colour, turn, move" rule) and adds what the brief's section 10 asks
for on top of it:

* :func:`parse_rule_string` - turns a compact rule string such as ``"RL"``,
  ``"LLRR"`` or ``"LRRRRLL"`` into the ``{colour: (next_colour, turn)}``
  dictionary that :class:`LangtonsAnt` already expects. Any string made only
  of the letters L/R is a valid rule; each character is one colour, cycling
  colour ``i -> i+1`` (mod length).
* :class:`AntAnalyzer` - measures step count, turn count, distinct cells
  visited, bounding box and a simple "highway" (periodic straight-line
  escape) detector, without changing how ``LangtonsAnt.step()`` behaves.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from tla_lab.utils.paths import ensure_legacy_paths_importable

ensure_legacy_paths_importable()

# Original, unmodified implementation.
from langton import LangtonsAnt  # noqa: E402

_RULE_RE = re.compile(r"^[LR]+$")


def parse_rule_string(rule: str) -> Dict[int, Tuple[int, str]]:
    """Convert a rule string like ``"RL"`` (the classic ant) or
    ``"LLRR"`` into the ``rules`` dict ``LangtonsAnt.__init__`` expects:
    ``{current_colour: (next_colour, turn_direction)}``.

    :raises ValueError: if ``rule`` is empty or contains characters other
        than 'L'/'R'.
    """
    rule = rule.strip().upper()
    if not rule or not _RULE_RE.match(rule):
        raise ValueError(
            f"Invalid Langton's Ant rule {rule!r}: must be a non-empty "
            "string made only of the letters 'L' and 'R' (e.g. 'RL', "
            "'LLRR', 'LRRRRLL')."
        )
    n = len(rule)
    return {i: ((i + 1) % n, rule[i]) for i in range(n)}


# A handful of well-known, named rules (their *letters*, not any claim about
# their long-term behaviour, which is only ever reported after an actual
# simulation run via AntAnalyzer).
KNOWN_RULES = {
    "RL (classic ant)": "RL",
    "RLR": "RLR",
    "LLRR (Highway builder)": "LLRR",
    "LRRRRLL": "LRRRRLL",
    "RRLL": "RRLL",
}


@dataclass
class AntAnalyzer:
    """Runs a :class:`LangtonsAnt` instance for a number of steps while
    recording statistics, without modifying the simulation logic itself."""

    ant: LangtonsAnt
    rule_string: str = ""
    steps_taken: int = 0
    turns_left: int = 0
    turns_right: int = 0
    visited: set = field(default_factory=set)
    min_r: int = field(default=None)
    max_r: int = field(default=None)
    min_c: int = field(default=None)
    max_c: int = field(default=None)

    def __post_init__(self):
        r, c = self.ant.get_current_position()
        self.visited.add((r, c))
        self.min_r = self.max_r = r
        self.min_c = self.max_c = c

    def step(self) -> None:
        r, c = self.ant.get_current_position()
        colour = int(self.ant.grid[r, c])
        turn_dir = self.ant.rules.get(colour, (colour, None))[1]

        self.ant.step()
        self.steps_taken += 1
        if turn_dir == "L":
            self.turns_left += 1
        elif turn_dir == "R":
            self.turns_right += 1

        nr, nc = self.ant.get_current_position()
        self.visited.add((nr, nc))
        self.min_r, self.max_r = min(self.min_r, nr), max(self.max_r, nr)
        self.min_c, self.max_c = min(self.min_c, nc), max(self.max_c, nc)

    def run(self, n_steps: int) -> None:
        for _ in range(n_steps):
            self.step()

    @property
    def bounding_box(self) -> Tuple[int, int, int, int]:
        """(min_row, min_col, max_row, max_col) of every cell the ant has
        touched so far."""
        return (self.min_r, self.min_c, self.max_r, self.max_c)

    @property
    def cells_visited(self) -> int:
        return len(self.visited)

    def color_counts(self) -> Dict[int, int]:
        """Count of grid cells currently at each colour value (0 = white in
        the classic 2-colour rule)."""
        import numpy as np
        values, counts = np.unique(self.ant.grid, return_counts=True)
        return dict(zip(values.tolist(), counts.tolist()))

    def looks_like_highway(self, window: int = 200, straightness_threshold: float = 0.9) -> bool:
        """Heuristic, *not* a proof: checks whether, over the last
        ``window`` steps, the ant's bounding box grew roughly linearly in
        one axis - a loose proxy for the well-known "highway" behaviour some
        rules exhibit after an initial chaotic phase. This never claims
        mathematical periodicity; it only reports a pattern observed in the
        steps actually simulated.
        """
        if self.steps_taken < window:
            return False
        span_r = self.max_r - self.min_r
        span_c = self.max_c - self.min_c
        span = max(span_r, span_c)
        return span >= straightness_threshold * self.steps_taken


__all__ = ["LangtonsAnt", "parse_rule_string", "KNOWN_RULES", "AntAnalyzer"]
