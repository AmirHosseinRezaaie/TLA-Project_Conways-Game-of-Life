# -*- coding: utf-8 -*-
"""
tla_lab.gui.main_menu
========================

The central "Computational Theory Laboratory" hub (brief section 4): a
single entry point from which the user reaches any of the five modules.
"""

from __future__ import annotations

from tla_lab.gui.app import Screen, Button, COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT

MODULES = [
    ("Turing Machine", "Tape / head / state visualizer, step & run modes"),
    ("Busy Beaver", "Run existing BB(1..5) machines + bounded 2-state search"),
    ("Conway's Game of Life", "Pattern editor, simulation, pattern library, benchmark"),
    ("Langton's Ant", "Rule selection, custom rules, live stats"),
    ("Logic Gates", "AND/NOT via real gliders; OR/NAND/NOR/XOR/Adders composed from them"),
]


def build_main_menu(open_module_callback):
    """Returns a factory ``(fonts) -> Screen`` for :class:`tla_lab.gui.app.App`.

    ``open_module_callback(index)`` is called with the index into
    :data:`MODULES` when a module button is clicked; the caller (``run_lab.py``)
    decides what screen replaces the menu.
    """

    class MainMenuScreen(Screen):
        title = "Computational Theory Laboratory"

        def __init__(self, fonts):
            super().__init__(fonts)
            self.buttons = []
            for i, (name, desc) in enumerate(MODULES):
                y = 150 + i * 90
                self.buttons.append(
                    Button((60, y, 300, 60), name, (lambda idx=i: open_module_callback(idx)))
                )
            self._descriptions = [d for _, d in MODULES]

        def handle_event(self, event):
            for b in self.buttons:
                b.handle_event(event)
            return None

        def update(self, dt: float) -> None:
            pass

        def draw(self, surface) -> None:
            f = self.fonts
            surface.blit(f["title"].render("Computational Theory Laboratory", True, COLOR_TEXT), (60, 40))
            surface.blit(f["small"].render(
                "Turing Machine -> Busy Beaver -> Game of Life -> Langton's Ant -> Logic Gates",
                True, COLOR_MUTED), (60, 90))
            for i, b in enumerate(self.buttons):
                b.draw(surface, f)
                desc = self._descriptions[i]
                surface.blit(f["small"].render(desc, True, COLOR_MUTED), (380, b.rect.y + 20))

    return MainMenuScreen
