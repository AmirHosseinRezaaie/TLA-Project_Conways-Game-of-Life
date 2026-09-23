# -*- coding: utf-8 -*-
"""
tla_lab.utils.paths
====================

The original project ships its code inside two folders whose names contain
spaces and an apostrophe:

    "Part 1 - Busy Beaver"
    "Part 2 - GoL & Langton's Ant"

Those names are perfectly valid *directories* but cannot be valid Python
*package* names, so they cannot be imported with a normal ``import`` or
``from package import module`` statement.

Rather than moving/renaming the student's original files (which section 1 of
the project brief explicitly forbids), this module adds both folders to
``sys.path`` at runtime. Once a directory is on ``sys.path`` its modules
(``turing_machine.py``, ``conway.py`` ...) become importable exactly as they
already are imported by the original test scripts that live next to them.

This is the single place in the whole ``tla_lab`` package that knows about
the on-disk layout of the legacy code, so if the folders are ever renamed,
only this file needs to change.
"""

from __future__ import annotations

import os
import sys

# Root of the whole repository (the folder that contains this file's
# grandparent, i.e. the directory that also contains "Part 1 - Busy Beaver").
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

PART1_DIR = os.path.join(PROJECT_ROOT, "Part 1 - Busy Beaver")
PART2_DIR = os.path.join(PROJECT_ROOT, "Part 2 - GoL & Langton's Ant")


def ensure_legacy_paths_importable() -> None:
    """Add the legacy Part 1 / Part 2 folders to ``sys.path`` (idempotent).

    Safe to call multiple times; only inserts a path once.
    """
    for path in (PART1_DIR, PART2_DIR):
        if os.path.isdir(path) and path not in sys.path:
            sys.path.insert(0, path)


def pattern_files():
    """Return the absolute paths of every ``.cells`` pattern file that ships
    with the original Part 2 folder."""
    if not os.path.isdir(PART2_DIR):
        return []
    return sorted(
        os.path.join(PART2_DIR, name)
        for name in os.listdir(PART2_DIR)
        if name.endswith(".cells") or name.endswith(".rle")
    )


# Importing this module always makes the legacy code importable - this keeps
# every call site (`from tla_lab.core... import ...`) simple.
ensure_legacy_paths_importable()
