# -*- coding: utf-8 -*-
"""
tla_lab.core.game_of_life
============================

Wraps the original ``Part 2 - GoL & Langton's Ant/conway.py``
(``GameOfLife`` class, ``parse_pattern`` loader for ``.cells``/``.rle``) and
adds the pieces the brief's section 7/8 ask for that the original module did
not have:

* :func:`save_cells` / :func:`save_rle` - the original module can *load*
  ``.cells``/``.rle`` but has no writer; these add one without touching
  ``conway.py``.
* :func:`randomize` - fills the grid with a random pattern (for the new
  Pattern Editor's "Randomize" button).
* :class:`GameOfLifeSession` - a thin stateful wrapper the GUI/benchmark use
  to track generation count and population history without re-deriving that
  bookkeeping in every caller (Normal Update vs Fast Update, Finite vs
  Toroidal boundary are exactly the ``fastMode`` / ``finite`` flags already
  implemented in ``conway.GameOfLife``, untouched here).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

from tla_lab.utils.paths import ensure_legacy_paths_importable

ensure_legacy_paths_importable()

# Original, unmodified implementation.
from conway import GameOfLife, parse_pattern  # noqa: E402


def randomize(gol: GameOfLife, density: float = 0.25, seed: int | None = None) -> None:
    """Fill ``gol.grid`` with live cells at the given density (0..1).

    Uses the same ``aliveValue`` / ``deadValue`` convention already defined
    on the ``GameOfLife`` instance, so it stays consistent with everything
    else ``conway.py`` does.
    """
    rng = np.random.default_rng(seed)
    mask = rng.random(gol.grid.shape) < density
    gol.grid[:] = np.where(mask, gol.aliveValue, gol.deadValue).astype(gol.grid.dtype)


def live_cells(gol: GameOfLife) -> List[Tuple[int, int]]:
    """Return (row, col) coordinates of every live cell, smallest bounding
    box first row/col - used by both the .cells/.rle writers and the GUI."""
    rows, cols = np.nonzero(gol.grid == gol.aliveValue)
    return list(zip(rows.tolist(), cols.tolist()))


def save_cells(gol: GameOfLife, filepath: str, name: str = "Untitled") -> None:
    """Write the current live cells as a plain-text ``.cells`` file
    (the format ``conway.parse_pattern`` already knows how to read back).

    Cells are cropped to their bounding box so the saved pattern is
    reusable at any grid size, matching how the shipped pattern files
    (glider, guns, ...) are structured.
    """
    cells = live_cells(gol)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"!Name: {name}\n")
        f.write("!Saved by TLA Computational Theory Laboratory\n")
        if not cells:
            return
        min_r = min(r for r, _ in cells)
        min_c = min(c for _, c in cells)
        max_r = max(r for r, _ in cells)
        max_c = max(c for _, c in cells)
        grid_out = [
            ["." for _ in range(max_c - min_c + 1)]
            for _ in range(max_r - min_r + 1)
        ]
        for r, c in cells:
            grid_out[r - min_r][c - min_c] = "O"
        for row in grid_out:
            f.write("".join(row) + "\n")


def save_rle(gol: GameOfLife, filepath: str, name: str = "Untitled") -> None:
    """Write the current live cells as a run-length-encoded ``.rle`` file,
    the second format ``conway.parse_pattern`` can already read back."""
    cells = live_cells(gol)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"#N {name}\n")
        f.write("#C Saved by TLA Computational Theory Laboratory\n")
        if not cells:
            f.write("x = 0, y = 0, rule = B3/S23\n!\n")
            return
        min_r = min(r for r, _ in cells)
        min_c = min(c for _, c in cells)
        max_r = max(r for r, _ in cells)
        max_c = max(c for _, c in cells)
        width = max_c - min_c + 1
        height = max_r - min_r + 1
        f.write(f"x = {width}, y = {height}, rule = B3/S23\n")

        live_set = {(r - min_r, c - min_c) for r, c in cells}
        lines = []
        for r in range(height):
            run_char = None
            run_len = 0
            row_tokens = []
            for c in range(width):
                ch = "o" if (r, c) in live_set else "b"
                if ch == run_char:
                    run_len += 1
                else:
                    if run_char is not None:
                        row_tokens.append(f"{run_len if run_len > 1 else ''}{run_char}")
                    run_char, run_len = ch, 1
            if run_char is not None:
                row_tokens.append(f"{run_len if run_len > 1 else ''}{run_char}")
            # Trailing dead cells on a row don't need to be encoded.
            line = "".join(row_tokens)
            line = line[:-1] if line.endswith("b") else line
            lines.append(line if line else "b")
        f.write("$\n".join(lines) + "!\n")


@dataclass
class GameOfLifeSession:
    """Stateful bookkeeping around a ``GameOfLife`` instance for the GUI and
    benchmark: generation counter + population history, nothing that
    ``conway.py`` itself needs to know about."""

    gol: GameOfLife
    generation: int = 0
    population_history: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.population_history.append(int(np.sum(self.gol.grid == self.gol.aliveValue)))

    @property
    def population(self) -> int:
        return int(np.sum(self.gol.grid == self.gol.aliveValue))

    def step(self) -> None:
        self.gol.tick()
        self.generation += 1
        self.population_history.append(self.population)

    def reset(self) -> None:
        self.gol.grid[:] = self.gol.deadValue
        self.generation = 0
        self.population_history = [0]


__all__ = [
    "GameOfLife", "parse_pattern", "randomize", "live_cells",
    "save_cells", "save_rle", "GameOfLifeSession",
]
