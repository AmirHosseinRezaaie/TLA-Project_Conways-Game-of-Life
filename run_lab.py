#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_lab.py
============

Entry point for the Computational Theory Laboratory GUI.

Usage:
    python run_lab.py

Requires pygame, numpy and scipy (see requirements.txt). This launches a
single Pygame window with a central menu; pick a module to enter it, press
[Esc] at any time to return to the menu, and close the window (or Alt+F4 /
Cmd+Q) to quit.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tla_lab.gui.app import App
from tla_lab.gui.main_menu import build_main_menu
from tla_lab.gui.turing_view import TuringMachineScreen
from tla_lab.gui.busy_beaver_view import BusyBeaverScreen
from tla_lab.gui.gol_view import GameOfLifeScreen
from tla_lab.gui.langton_view import LangtonAntScreen
from tla_lab.gui.logic_gates_view import LogicGatesScreen

MODULE_SCREENS = [
    TuringMachineScreen,
    BusyBeaverScreen,
    GameOfLifeScreen,
    LangtonAntScreen,
    LogicGatesScreen,
]


def main():
    app_ref = {}

    def open_module(index: int):
        app = app_ref["app"]
        screen_cls = MODULE_SCREENS[index]
        app.current = screen_cls(app.fonts)

    menu_factory = build_main_menu(open_module)
    app = App(menu_factory, title="Computational Theory Laboratory")
    app_ref["app"] = app
    app.run()


if __name__ == "__main__":
    main()
