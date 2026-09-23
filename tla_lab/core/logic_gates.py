# -*- coding: utf-8 -*-
"""
tla_lab.core.logic_gates
============================

The original ``Part 2 - GoL & Langton's Ant/logic_gates.py`` implements
``AND`` and ``NOT`` by literally firing gliders into each other inside a
``conway.GameOfLife`` grid and inspecting the surviving debris (a stationary
block = a formed signal, a surviving 5-cell glider = the untouched control
signal). That class, :class:`GliderLogicGates`, is imported here unmodified.

Design decision for OR / NAND / NOR / XOR (brief section 9)
-------------------------------------------------------------
Hand-crafting *new* glider collision geometries for OR/NAND/NOR/XOR would
require placing gliders at exact new coordinates/phases and empirically
tuning them until the collision produces the right debris - exactly what the
original AND/NOT gates in this project already do. Doing that reliably for
four more gates, *without* being able to run Pygame/visually inspect the
collisions in this environment, is not something that can be verified here.

Rather than fabricate untested collision coordinates and present them as
working glider circuits (which would violate the "no unproven claims"
requirement in the brief), the extra gates are built by **composing calls to
the already-validated ``run_and_gate`` / ``run_not_gate`` simulations**,
using the standard Boolean identities:

    OR(a, b)   = NOT(AND(NOT(a), NOT(b)))            (De Morgan)
    NAND(a, b) = NOT(AND(a, b))
    NOR(a, b)  = NOT(OR(a, b))
    XOR(a, b)  = OR(AND(a, NOT(b)), AND(NOT(a), b))

Every one of those calls still runs a *real* Game of Life simulation at the
leaf level (there is no shortcut Python ``and``/``or`` anywhere in the
truth-table computation) - it is simply the composition, not the primitive
collision geometry, that is new. This is stated explicitly here and in the
README so nobody mistakes this for a single native glider circuit; it is a
circuit *of* validated glider gates, the same way real logic circuits are
built out of validated primitive gates.

Half/Full Adder (brief section 9, Priority 3) are built the same way, using
the standard combinational-logic definitions on top of XOR/AND above.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from tla_lab.utils.paths import ensure_legacy_paths_importable

ensure_legacy_paths_importable()

# Original, unmodified implementation (real glider-collision AND / NOT).
from logic_gates import GliderLogicGates  # noqa: E402

_gates = GliderLogicGates()


def gol_and(a: bool, b: bool) -> bool:
    """Native glider-collision AND gate (unchanged from Part 2)."""
    return _gates.run_and_gate(input_a_present=a, input_b_present=b)


def gol_not(a: bool) -> bool:
    """Native glider-collision NOT gate (unchanged from Part 2)."""
    return _gates.run_not_gate(input_a_present=a)


def gol_or(a: bool, b: bool) -> bool:
    """OR, composed from the two validated glider gates above via
    De Morgan's law: OR(a, b) = NOT(AND(NOT(a), NOT(b)))."""
    return gol_not(gol_and(gol_not(a), gol_not(b)))


def gol_nand(a: bool, b: bool) -> bool:
    """NAND, composed as NOT(AND(a, b))."""
    return gol_not(gol_and(a, b))


def gol_nor(a: bool, b: bool) -> bool:
    """NOR, composed as NOT(OR(a, b))."""
    return gol_not(gol_or(a, b))


def gol_xor(a: bool, b: bool) -> bool:
    """XOR, composed as OR(AND(a, NOT b), AND(NOT a, b))."""
    return gol_or(gol_and(a, gol_not(b)), gol_and(gol_not(a), b))


GATES: Dict[str, Callable[..., bool]] = {
    "AND": gol_and,
    "NOT": gol_not,
    "OR": gol_or,
    "NAND": gol_nand,
    "NOR": gol_nor,
    "XOR": gol_xor,
}

_BINARY_GATES = {"AND", "OR", "NAND", "NOR", "XOR"}


def truth_table(gate_name: str) -> List[Tuple]:
    """Return the truth table of ``gate_name`` computed by *actually
    running* the (possibly composed) glider simulation for every input
    combination - nothing here is a hard-coded lookup table."""
    fn = GATES[gate_name]
    if gate_name == "NOT":
        return [(a, fn(a)) for a in (False, True)]
    return [(a, b, fn(a, b)) for a in (False, True) for b in (False, True)]


@dataclass
class AdderResult:
    sum_bit: bool
    carry_out: bool


def half_adder(a: bool, b: bool) -> AdderResult:
    """Standard half-adder: sum = XOR(a, b), carry = AND(a, b). Both
    building blocks are the glider gates above, so the result of a Half
    Adder here is the composition of several real GoL simulations."""
    return AdderResult(sum_bit=gol_xor(a, b), carry_out=gol_and(a, b))


def full_adder(a: bool, b: bool, carry_in: bool) -> AdderResult:
    """Standard full-adder built from two half adders + one OR, all on top
    of the glider primitives: sum = a XOR b XOR cin,
    carry_out = (a AND b) OR (cin AND (a XOR b))."""
    h1 = half_adder(a, b)
    h2 = half_adder(h1.sum_bit, carry_in)
    carry_out = gol_or(h1.carry_out, h2.carry_out)
    return AdderResult(sum_bit=h2.sum_bit, carry_out=carry_out)


def four_bit_adder(a_bits: List[bool], b_bits: List[bool]) -> Tuple[List[bool], bool]:
    """Ripple-carry 4-bit adder built from four :func:`full_adder` calls
    (least-significant bit first). Returns (sum_bits, final_carry_out).

    Because every bit position triggers real Game of Life simulations, this
    call performs dozens of simulated generations end-to-end - it is a
    genuine (if slow) demonstration that Life's local rules are sufficient
    to build arbitrary combinational logic, not just an illustration.
    """
    if len(a_bits) != 4 or len(b_bits) != 4:
        raise ValueError("four_bit_adder expects exactly 4 bits per operand.")
    carry = False
    sum_bits: List[bool] = []
    for a, b in zip(a_bits, b_bits):
        r = full_adder(a, b, carry)
        sum_bits.append(r.sum_bit)
        carry = r.carry_out
    return sum_bits, carry


__all__ = [
    "GliderLogicGates", "gol_and", "gol_not", "gol_or", "gol_nand",
    "gol_nor", "gol_xor", "GATES", "truth_table", "AdderResult",
    "half_adder", "full_adder", "four_bit_adder",
]
