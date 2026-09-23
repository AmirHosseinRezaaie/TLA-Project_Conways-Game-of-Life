# -*- coding: utf-8 -*-
"""Tests for tla_lab.core.busy_beaver — wraps Part 1's busy_beaver.py."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tla_lab.core.busy_beaver import (
    run_beaver, available_state_counts, BusyBeaverSearch,
)


def test_available_state_counts_matches_project_table():
    counts = available_state_counts()
    assert counts == [1, 2, 3, 4, 5]


def test_bb2_halts_and_matches_project_program():
    result = run_beaver(2)
    assert result.halted is True
    assert result.steps == 6
    assert result.ones_written == 4


def test_bb_all_shipped_machines_halt():
    for n in available_state_counts():
        result = run_beaver(n)
        assert result.halted is True
        assert result.ones_written > 0
        assert result.steps > 0


def test_invalid_state_count_raises():
    import pytest
    with pytest.raises(ValueError):
        run_beaver(0)
    with pytest.raises(ValueError):
        run_beaver(99)


def test_search_respects_step_limit_and_timeout():
    # Extremely small timeout must still return promptly with a well-formed
    # SearchProgress object, never hang.
    search = BusyBeaverSearch(n_states=2, step_limit=20, timeout_s=1.0)
    progress = search.run()
    assert progress.machines_tried > 0
    assert progress.elapsed_seconds < 3.0  # generous margin over the 1s timeout


def test_search_can_be_cancelled():
    search = BusyBeaverSearch(n_states=2, step_limit=200, timeout_s=30.0)
    search.cancel()  # cancel before even starting
    progress = search.run()
    assert progress.cancelled is True


def test_search_2state_finds_the_known_bb2_result():
    # The 2-state Busy Beaver's best halting machine writes 4 ones in 6
    # steps - this is well established and small enough to brute-force
    # exhaustively within a few seconds.
    search = BusyBeaverSearch(n_states=2, step_limit=100, timeout_s=15.0)
    progress = search.run()
    assert progress.best_ones == 4
    assert progress.best_steps == 6
