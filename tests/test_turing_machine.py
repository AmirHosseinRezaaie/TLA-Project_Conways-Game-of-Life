# -*- coding: utf-8 -*-
"""Tests for tla_lab.core.turing_machine — wraps Part 1's TuringMachine."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tla_lab.core.turing_machine import TuringMachine, trace, format_tape


def test_accepts_double_hash():
    tm = TuringMachine({
        ("q0", "#"): ("saw_#", "#", "R"),
        ("saw_#", "#"): ("saw_##", "#", "R"),
        ("saw_##", ""): ("qa", "", "R"),
    })
    assert tm.accepts("##") is True
    assert tm.accepts("#") is None or tm.accepts("#") is False


def test_rejects_wrong_input():
    tm = TuringMachine({
        ("q0", "#"): ("saw_#", "#", "R"),
        ("saw_#", ""): ("qa", "", "R"),
    })
    assert tm.accepts("#") is True
    assert tm.accepts("##") is False


def test_transition_and_halt_detection():
    tm = TuringMachine({
        ("q0", "1"): ("qa", "1", "R"),
    })
    history = trace(tm, "1", step_limit=10)
    actions = [a for a, _ in history]
    assert "Accept" in actions


def test_step_limit_prevents_infinite_loop():
    # A machine that keeps moving right forever, with a transition defined
    # for both '1' and the blank symbol, so it never hits an undefined
    # transition (which the engine treats as an implicit Reject) and never
    # reaches an explicit accept/reject state either.
    tm = TuringMachine({
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", ""): ("q0", "", "R"),
    })
    # accepts() must return None (not hang) when the step limit is hit.
    result = tm.accepts("1" * 5, step_limit=20)
    assert result is None


def test_unary_addition_like_machine():
    # 1+1 in unary with a '0' delimiter, consumed by moving right over 1s,
    # replacing the delimiter with blank, and moving left back - mirrors the
    # structure of Part 1/test_turing_adder.py without importing it (that
    # script relies on being executed from its own directory).
    transitions = {
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "0"): ("q_back", "", "L"),
        ("q_back", "1"): ("qa", "1", "R"),
    }
    tm = TuringMachine(transitions)
    result = list(tm.run("110"))
    assert result[-1][0] == "Accept"


def test_format_tape_places_head_marker():
    tm = TuringMachine({("q0", "1"): ("qa", "1", "R")})
    history = trace(tm, "1")
    rendered = format_tape(history[0][1])
    assert "[" in rendered and "]" in rendered
