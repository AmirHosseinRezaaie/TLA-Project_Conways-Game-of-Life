# -*- coding: utf-8 -*-
"""
tla_lab.core.turing_machine
============================

This module does **not** re-implement the Turing machine. It imports the
original, already-working ``TuringMachine`` class from
``Part 1 - Busy Beaver/turing_machine.py`` and adds a small amount of
convenience code that the GUI visualizer (section 5 of the brief) needs:

* :func:`trace` - runs the machine and returns the *full* list of
  ``(action, configuration)`` steps up to ``step_limit``, so the visualizer
  can let the user scrub forward/backward without re-running the machine.
* :class:`StepLimitReached` - a small marker exception used by the GUI layer
  to distinguish "ran out of steps" from "the machine actually halted".

Everything else (tape/head/state representation, generator design, accept /
reject detection, ``debug()``...) is exactly the class shipped in Part 1.
"""

from __future__ import annotations

from typing import List, Tuple, Dict, Any

from tla_lab.utils.paths import ensure_legacy_paths_importable

ensure_legacy_paths_importable()

# Import the original, unmodified implementation.
from turing_machine import TuringMachine  # noqa: E402  (import after sys.path fix)


class StepLimitReached(Exception):
    """Raised by :func:`trace` (never by the original class) when the
    machine did not halt within ``step_limit`` steps."""


def trace(machine: TuringMachine, input_: str, step_limit: int = 500) -> List[Tuple[str, Dict[str, Any]]]:
    """Materialize the machine's generator-based execution into a list.

    The original :class:`TuringMachine`. ``run()`` is a *generator*
    (see the docstring in ``turing_machine.py`` for why). That laziness is
    perfect for programmatic use (``accepts`` / ``rejects``), but a
    step-by-step / scrub-back-and-forth visualizer needs the whole history
    at once. This helper simply drains the generator, honouring the same
    ``step_limit`` semantics as :meth:`TuringMachine.accepts`.

    :param machine: an already constructed ``TuringMachine``.
    :param input_: the tape input, string or list of symbols.
    :param step_limit: safety cap so a non-halting machine cannot freeze
        the GUI.
    :return: list of ``(action, configuration)`` tuples, oldest first.
    """
    history: List[Tuple[str, Dict[str, Any]]] = []
    for i, (action, config) in enumerate(machine.run(input_)):
        history.append((action, config))
        if action in ("Accept", "Reject"):
            return history
        if i + 1 >= step_limit:
            break
    return history


def format_tape(config: Dict[str, Any]) -> str:
    """Render a configuration dict as a single human-readable tape string
    with the head position marked in ``[brackets]``, e.g. ``0011[1]010``.

    Used by both the terminal ``debug()`` (already in Part 1) and the new
    Pygame visualizer, so the formatting logic lives in exactly one place.
    """
    left = "".join(config["left_hand_side"])
    right = "".join(config["right_hand_side"])
    return f'{left}[{config["symbol"]}]{right}'


__all__ = ["TuringMachine", "StepLimitReached", "trace", "format_tape"]
