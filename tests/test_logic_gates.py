# -*- coding: utf-8 -*-
"""Tests for tla_lab.core.logic_gates — wraps Part 2's logic_gates.py.

These tests actually run the Game of Life glider simulations (they are not
mocked), so they are slower than the other test modules but are the real
end-to-end proof that the composed gates behave like their Boolean namesakes.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tla_lab.core.logic_gates import (
    gol_and, gol_not, gol_or, gol_nand, gol_nor, gol_xor,
    half_adder, full_adder, four_bit_adder, truth_table,
)


def test_and_gate_truth_table():
    assert gol_and(False, False) is False
    assert gol_and(False, True) is False
    assert gol_and(True, False) is False
    assert gol_and(True, True) is True


def test_not_gate_truth_table():
    assert gol_not(False) is True
    assert gol_not(True) is False


def test_or_gate_truth_table():
    assert gol_or(False, False) is False
    assert gol_or(False, True) is True
    assert gol_or(True, False) is True
    assert gol_or(True, True) is True


def test_nand_gate_truth_table():
    assert gol_nand(True, True) is False
    assert gol_nand(True, False) is True
    assert gol_nand(False, False) is True


def test_nor_gate_truth_table():
    assert gol_nor(False, False) is True
    assert gol_nor(True, False) is False
    assert gol_nor(True, True) is False


def test_xor_gate_truth_table():
    assert gol_xor(False, False) is False
    assert gol_xor(True, True) is False
    assert gol_xor(True, False) is True
    assert gol_xor(False, True) is True


def test_truth_table_helper_matches_direct_calls():
    tt = truth_table("AND")
    assert (False, False, False) in tt
    assert (True, True, True) in tt


def test_half_adder_arithmetic():
    r = half_adder(True, True)
    assert r.sum_bit is False and r.carry_out is True   # 1+1 = 10
    r0 = half_adder(False, True)
    assert r0.sum_bit is True and r0.carry_out is False  # 0+1 = 01


def test_full_adder_arithmetic():
    r = full_adder(True, True, True)  # 1+1+1 = 11
    assert r.sum_bit is True and r.carry_out is True


def test_four_bit_adder_computes_correct_sum():
    # 13 (1101 LSB-first: [1,0,1,1]) + 6 (0110 LSB-first: [0,1,1,0]) = 19
    a_bits = [True, False, True, True]
    b_bits = [False, True, True, False]
    sum_bits, carry = four_bit_adder(a_bits, b_bits)
    value = sum(bit * (2 ** i) for i, bit in enumerate(sum_bits)) + carry * 16
    assert value == 19
