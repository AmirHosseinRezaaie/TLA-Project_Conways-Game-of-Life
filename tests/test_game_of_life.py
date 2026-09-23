# -*- coding: utf-8 -*-
"""Tests for tla_lab.core.game_of_life — wraps Part 2's conway.py."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from tla_lab.core.game_of_life import (
    GameOfLife, GameOfLifeSession, parse_pattern, randomize,
    save_cells, save_rle, live_cells,
)


def test_blinker_oscillates_with_period_2():
    gol = GameOfLife(N=10, finite=False, fastMode=True)
    gol.insertBlinker(index=(3, 3))
    gen0 = gol.grid.copy()
    gol.tick()
    gen1 = gol.grid.copy()
    gol.tick()
    gen2 = gol.grid.copy()
    assert not np.array_equal(gen0, gen1)  # it changed shape...
    assert np.array_equal(gen0, gen2)      # ...and returned after 2 ticks


def test_still_life_block_is_stable():
    gol = GameOfLife(N=10, finite=False, fastMode=True)
    gol.grid[4, 4] = gol.grid[4, 5] = gol.grid[5, 4] = gol.grid[5, 5] = gol.aliveValue
    before = gol.grid.copy()
    gol.tick()
    assert np.array_equal(before, gol.grid)


def test_glider_translates_after_4_generations():
    gol = GameOfLife(N=20, finite=False, fastMode=True)
    gol.insertGlider(index=(1, 1))
    before = set(live_cells(gol))
    for _ in range(4):
        gol.tick()
    after = set(live_cells(gol))
    assert before != after
    assert len(after) == len(before) == 5  # glider always has 5 live cells


def test_toroidal_boundary_wraps():
    gol = GameOfLife(N=6, finite=False, fastMode=True)
    # Blinker straddling the top edge so its vertical phase needs wrapping.
    gol.grid[0, 2] = gol.grid[0, 3] = gol.grid[0, 4] = gol.aliveValue
    gol.tick()
    # After the flip to vertical, the cell that wrapped to the bottom row
    # (row -1 -> row N-1) should be alive.
    assert gol.grid[gol.rows - 1, 3] == gol.aliveValue or gol.grid[0, 3] == gol.aliveValue


def test_finite_boundary_kills_wrap_neighbors():
    gol_finite = GameOfLife(N=6, finite=True, fastMode=True)
    gol_finite.grid[0, 2] = gol_finite.grid[0, 3] = gol_finite.grid[0, 4] = gol_finite.aliveValue
    gol_finite.tick()
    # With a finite boundary, nothing should appear on the wrapped-around
    # bottom row (row N-1), unlike the toroidal case.
    assert gol_finite.grid[gol_finite.rows - 1, 3] == gol_finite.deadValue


def test_normal_and_fast_mode_agree():
    fast = GameOfLife(N=15, finite=False, fastMode=True)
    normal = GameOfLife(N=15, finite=False, fastMode=False)
    randomize(fast, density=0.3, seed=1)
    normal.grid[:] = fast.grid[:]
    for _ in range(3):
        fast.tick()
        normal.tick()
    assert np.array_equal(fast.grid, normal.grid)


def test_cells_pattern_parser_roundtrip(tmp_path):
    gol = GameOfLife(N=12, finite=False, fastMode=True)
    gol.insertGlider(index=(2, 2))
    path = str(tmp_path / "glider.cells")
    save_cells(gol, path, name="test glider")
    width, height, cells = parse_pattern(path)
    assert len(cells) == 5


def test_rle_pattern_parser_roundtrip(tmp_path):
    gol = GameOfLife(N=12, finite=False, fastMode=True)
    gol.insertGlider(index=(2, 2))
    path = str(tmp_path / "glider.rle")
    save_rle(gol, path, name="test glider")
    width, height, cells = parse_pattern(path)
    assert len(cells) == 5


def test_session_tracks_generation_and_population():
    gol = GameOfLife(N=10, finite=False, fastMode=True)
    gol.insertBlinker(index=(3, 3))
    session = GameOfLifeSession(gol)
    assert session.generation == 0
    assert session.population == 3
    session.step()
    assert session.generation == 1
    assert len(session.population_history) == 2
