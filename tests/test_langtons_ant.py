# -*- coding: utf-8 -*-
"""Tests for tla_lab.core.langtons_ant — wraps Part 2's langton.py."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from tla_lab.core.langtons_ant import LangtonsAnt, parse_rule_string, AntAnalyzer


def test_parse_classic_rl_rule():
    rules = parse_rule_string("RL")
    assert rules == {0: (1, "R"), 1: (0, "L")}


def test_parse_llrr_rule_has_4_colours():
    rules = parse_rule_string("LLRR")
    assert len(rules) == 4
    assert rules[3] == (0, "R")  # wraps back to colour 0


def test_parse_rule_rejects_invalid_characters():
    with pytest.raises(ValueError):
        parse_rule_string("RLX")
    with pytest.raises(ValueError):
        parse_rule_string("")


def test_ant_moves_on_first_step():
    ant = LangtonsAnt(N=20, ant_position=(10, 10), rules=parse_rule_string("RL"))
    start = ant.get_current_position()
    ant.step()
    assert ant.get_current_position() != start


def test_ant_turns_right_on_white_classic_rule():
    ant = LangtonsAnt(N=20, ant_position=(10, 10), rules=parse_rule_string("RL"))
    assert ant.direction == 0  # starts facing North
    ant.step()  # on white (0), classic rule turns Right
    assert ant.direction == 1  # East


def test_toroidal_wrap_at_grid_edge():
    ant = LangtonsAnt(N=5, ant_position=(0, 0), rules=parse_rule_string("RL"))
    ant.direction = 0  # facing North; one more step North wraps to row N-1
    ant.step()
    r, c = ant.get_current_position()
    assert 0 <= r < 5 and 0 <= c < 5  # never escapes the grid


def test_analyzer_tracks_bounding_box_and_visits():
    ant = LangtonsAnt(N=40, ant_position=(20, 20), rules=parse_rule_string("RL"))
    analyzer = AntAnalyzer(ant, rule_string="RL")
    analyzer.run(100)
    assert analyzer.steps_taken == 100
    assert analyzer.cells_visited >= 1
    min_r, min_c, max_r, max_c = analyzer.bounding_box
    assert min_r <= 20 <= max_r
    assert min_c <= 20 <= max_c


def test_analyzer_turn_counts_sum_to_steps():
    ant = LangtonsAnt(N=40, ant_position=(20, 20), rules=parse_rule_string("LLRR"))
    analyzer = AntAnalyzer(ant, rule_string="LLRR")
    analyzer.run(50)
    assert analyzer.turns_left + analyzer.turns_right == 50
