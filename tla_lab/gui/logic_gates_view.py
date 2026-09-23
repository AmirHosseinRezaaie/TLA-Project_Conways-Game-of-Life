# -*- coding: utf-8 -*-
"""
tla_lab.gui.logic_gates_view
===============================

Logic Gates screen (brief section 9). Every gate result shown here is the
output of an *actual* Game of Life glider-collision simulation (AND/NOT
natively, OR/NAND/NOR/XOR composed from them - see
``tla_lab.core.logic_gates`` for the full design rationale), never a plain
Python boolean shortcut.
"""

from __future__ import annotations

import threading

import pygame

from tla_lab.gui.app import Screen, Button, COLOR_TEXT, COLOR_MUTED, COLOR_PANEL, COLOR_OK, COLOR_DANGER, COLOR_ACCENT
from tla_lab.core.logic_gates import GATES, truth_table, half_adder, full_adder

GATE_NAMES = ["AND", "NOT", "OR", "NAND", "NOR", "XOR"]


class LogicGatesScreen(Screen):
    title = "Logic Gates (Glider-based)"

    def __init__(self, fonts):
        super().__init__(fonts)
        self.gate_index = 0
        self.input_a = False
        self.input_b = False
        self.output = None
        self.busy = False
        self.table = None
        self.adder_result = None
        self._menu_requested = False

        self.buttons = [
            Button((30, 100, 40, 36), "<", self._prev_gate),
            Button((80, 100, 40, 36), ">", self._next_gate),
            Button((150, 100, 110, 36), "Toggle A", self._toggle_a),
            Button((270, 100, 110, 36), "Toggle B", self._toggle_b),
            Button((400, 100, 160, 36), "Run Simulation", self._run_gate),
            Button((580, 100, 180, 36), "Compute Truth Table", self._run_truth_table),
            Button((30, 300, 220, 36), "Half Adder Demo", self._run_half_adder),
            Button((260, 300, 220, 36), "Full Adder Demo", self._run_full_adder),
            Button((780, 620, 190, 40), "Back to Menu", self._go_menu),
        ]

    @property
    def gate_name(self):
        return GATE_NAMES[self.gate_index]

    def _prev_gate(self):
        self.gate_index = (self.gate_index - 1) % len(GATE_NAMES)
        self.output = self.table = self.adder_result = None

    def _next_gate(self):
        self.gate_index = (self.gate_index + 1) % len(GATE_NAMES)
        self.output = self.table = self.adder_result = None

    def _toggle_a(self):
        self.input_a = not self.input_a

    def _toggle_b(self):
        self.input_b = not self.input_b

    def _run_gate(self):
        if self.busy:
            return
        gate_fn = GATES[self.gate_name]
        a, b = self.input_a, self.input_b

        def worker():
            self.busy = True
            result = gate_fn(a) if self.gate_name == "NOT" else gate_fn(a, b)
            self.output = result
            self.busy = False

        threading.Thread(target=worker, daemon=True).start()

    def _run_truth_table(self):
        if self.busy:
            return
        name = self.gate_name

        def worker():
            self.busy = True
            self.table = truth_table(name)
            self.busy = False

        threading.Thread(target=worker, daemon=True).start()

    def _run_half_adder(self):
        if self.busy:
            return

        def worker():
            self.busy = True
            r = half_adder(self.input_a, self.input_b)
            self.adder_result = ("Half Adder", f"sum={r.sum_bit} carry={r.carry_out}")
            self.busy = False

        threading.Thread(target=worker, daemon=True).start()

    def _run_full_adder(self):
        if self.busy:
            return

        def worker():
            self.busy = True
            r = full_adder(self.input_a, self.input_b, True)
            self.adder_result = ("Full Adder (carry_in=True)", f"sum={r.sum_bit} carry={r.carry_out}")
            self.busy = False

        threading.Thread(target=worker, daemon=True).start()

    def _go_menu(self):
        self._menu_requested = True

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        if self._menu_requested:
            return "menu"
        return None

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface) -> None:
        f = self.fonts
        surface.blit(f["title"].render(self.title, True, COLOR_TEXT), (30, 20))
        surface.blit(f["small"].render(
            "AND/NOT are real glider collisions. OR/NAND/NOR/XOR are circuits "
            "built by composing those two validated gates (see core/logic_gates.py).",
            True, COLOR_MUTED), (30, 60))

        surface.blit(f["heading"].render(f"Gate: {self.gate_name}", True, COLOR_ACCENT), (30, 155))
        a_text = "A = 1" if self.input_a else "A = 0"
        b_text = "B = 1" if self.input_b else "B = 0"
        surface.blit(f["body"].render(a_text, True, COLOR_TEXT), (30, 195))
        if self.gate_name != "NOT":
            surface.blit(f["body"].render(b_text, True, COLOR_TEXT), (150, 195))

        status = "Simulating..." if self.busy else "Idle"
        surface.blit(f["small"].render(f"Status: {status}", True, COLOR_MUTED), (30, 230))

        if self.output is not None:
            color = COLOR_OK if self.output else COLOR_DANGER
            surface.blit(f["heading"].render(f"Output = {int(self.output)}", True, color), (30, 260))

        # Truth table
        if self.table:
            pygame.draw.rect(surface, COLOR_PANEL, (400, 190, 300, 200), border_radius=8)
            surface.blit(f["body"].render("Truth table", True, COLOR_TEXT), (415, 200))
            for i, row in enumerate(self.table):
                surface.blit(f["mono"].render(str(row), True, COLOR_TEXT), (415, 230 + i * 24))

        if self.adder_result:
            name, text = self.adder_result
            surface.blit(f["body"].render(f"{name}: {text}", True, COLOR_TEXT), (30, 350))

        for b in self.buttons:
            b.draw(surface, f)
