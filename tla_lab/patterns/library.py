# -*- coding: utf-8 -*-
"""
tla_lab.patterns.library
==========================

A small catalog describing the Game of Life pattern files that already ship
in ``Part 2 - GoL & Langton's Ant/`` (brief section 8). No pattern files are
moved or duplicated; this module only attaches metadata (category, human
description) to the existing ``.cells`` files and computes size/population
by actually parsing them with the project's own ``conway.parse_pattern``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from tla_lab.utils.paths import PART2_DIR, pattern_files
from tla_lab.core.game_of_life import parse_pattern

# Hand-written descriptions for the patterns that ship with the project.
# Category follows the standard Life pattern taxonomy: Still Life,
# Oscillator, Spaceship, Gun, Logic, Other.
_METADATA = {
    "3enginecordership gun 279x258.cells": (
        "Gun", "A large 3-engine Cordership gun: a gun-type pattern that "
        "periodically emits Cordership spaceships."),
    "7enginecordership spaceship.cells": (
        "Spaceship", "A 7-engine Cordership: a large, fast-moving spaceship "
        "built from multiple synchronized 'engines'."),
    "ak94 gun.cells": (
        "Gun", "The AK94 gun, a compact glider/spaceship gun."),
    "dragon spaceship.cells": (
        "Spaceship", "The Dragon: an elementary orthogonal spaceship."),
    "stargate oscillator.cells": (
        "Oscillator", "Stargate: a large high-period oscillator."),
    "vacuumgun gun.cells": (
        "Gun", "A 'vacuum' gun pattern that emits gliders while leaving a "
        "clean exhaust behind it."),
}

# Patterns built directly by GameOfLife's own insert*() methods (no file on
# disk); listed here so the library/GUI can show the *complete* picture of
# what the project already supports, per brief section 3 ("Glider, Blinker,
# other existing patterns").
_BUILT_IN = {
    "Blinker (insertBlinker)": ("Oscillator", "The simplest oscillator: a "
        "row of three cells that flips between horizontal and vertical."),
    "Glider (insertGlider)": ("Spaceship", "The smallest, most common "
        "spaceship; translates diagonally by (1,1) every 4 generations."),
    "Gosper-style Glider Gun (insertGliderGun)": ("Gun", "A glider gun "
        "construct; the project's own docstring notes its coordinates may "
        "need debugging to loop correctly - preserved here as-is, unmodified."),
}


@dataclass
class PatternInfo:
    name: str
    category: str
    description: str
    filepath: Optional[str]
    width: Optional[int] = None
    height: Optional[int] = None
    population: Optional[int] = None
    built_in: bool = False


def list_patterns() -> List[PatternInfo]:
    """Return metadata for every pattern the project ships: both the
    ``.cells``/``.rle`` files in Part 2 and the built-in inserter methods on
    ``GameOfLife``. File-based patterns are actually parsed (via the
    project's own ``parse_pattern``) to report real width/height/population,
    not guessed values.
    """
    infos: List[PatternInfo] = []

    for path in pattern_files():
        import os
        fname = os.path.basename(path)
        category, description = _METADATA.get(fname, ("Other", "Pattern file shipped with the project."))
        try:
            width, height, live_cells = parse_pattern(path)
            population = len(live_cells)
        except Exception:
            width = height = population = None
        infos.append(PatternInfo(
            name=fname, category=category, description=description,
            filepath=path, width=width, height=height, population=population,
        ))

    for name, (category, description) in _BUILT_IN.items():
        infos.append(PatternInfo(
            name=name, category=category, description=description,
            filepath=None, built_in=True,
        ))

    return sorted(infos, key=lambda p: (p.category, p.name))


def categories() -> List[str]:
    return sorted({p.category for p in list_patterns()})


__all__ = ["PatternInfo", "list_patterns", "categories"]
