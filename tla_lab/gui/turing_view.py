# -*- coding: utf-8 -*-
"""
tla_lab.gui.turing_view
==========================

Turing Machine visualizer (brief section 5): shows the tape, head, current
state/symbol and the transition just taken, and supports both step-by-step
and automatic (speed-controlled) execution, built entirely on top of the
unmodified ``TuringMachine`` from Part 1 via ``tla_lab.core.turing_machine``.
"""

from __future__ import annotations

import pygame

from tla_lab.gui.app import (
    Screen, Button, COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT, COLOR_PANEL,
    COLOR_ALIVE, COLOR_DEAD, COLOR_OK, COLOR_DANGER,
)
from tla_lab.core.turing_machine import TuringMachine, trace, format_tape

# A handful of ready-to-run example machines (the same logic as the
# project's own test_turing_machine_example*.py scripts), so the GUI is
# usable without hand-typing a transition table.
EXAMPLE_MACHINES = {
    "Accepts '##'": dict(
        input_="##",
        transitions={
            ("q0", "#"): ("saw_#", "#", "R"),
            ("saw_#", "#"): ("saw_##", "#", "R"),
            ("saw_##", ""): ("qa", "", "R"),
        },
    ),
    "Accepts only '#'": dict(
        input_="#",
        transitions={
            ("q0", "#"): ("saw_#", "#", "R"),
            ("saw_#", ""): ("qa", "", "R"),
        },
    ),
}


class TuringMachineScreen(Screen):
    title = "Turing Machine Visualizer"

    def __init__(self, fonts):
        super().__init__(fonts)
        self.machine_name = list(EXAMPLE_MACHINES.keys())[0]
        self.history = []
        self.step_index = 0
        self.running_auto = False
        self.speed = 4  # steps per second while running automatically
        self._time_accum = 0.0
        self._load_machine(self.machine_name)

        self.buttons = [
            Button((30, 620, 90, 40), "Step", self._step_forward),
            Button((130, 620, 90, 40), "Run", self._toggle_run),
            Button((230, 620, 90, 40), "Pause", self._pause),
            Button((330, 620, 90, 40), "Reset", self._reset),
            Button((430, 620, 90, 40), "Stop", self._stop),
            Button((560, 620, 40, 40), "-", self._slower),
            Button((650, 620, 40, 40), "+", self._faster),
            Button((770, 620, 170, 40), "Back to Menu", self._go_menu),
        ]
        self._menu_requested = False

    # -- machine control ---------------------------------------------------
    def _load_machine(self, name):
        spec = EXAMPLE_MACHINES[name]
        self.machine_name = name
        self.machine = TuringMachine(spec["transitions"])
        self.input_ = spec["input_"]
        self.history = trace(self.machine, self.input_, step_limit=500)
        self.step_index = 0
        self.running_auto = False

    def _step_forward(self):
        if self.step_index < len(self.history) - 1:
            self.step_index += 1

    def _toggle_run(self):
        self.running_auto = True

    def _pause(self):
        self.running_auto = False

    def _reset(self):
        self.step_index = 0
        self.running_auto = False

    def _stop(self):
        self.running_auto = False
        self.step_index = 0

    def _slower(self):
        self.speed = max(1, self.speed - 1)

    def _faster(self):
        self.speed = min(30, self.speed + 1)

    def _go_menu(self):
        self._menu_requested = True

    def _cycle_machine(self):
        names = list(EXAMPLE_MACHINES.keys())
        idx = (names.index(self.machine_name) + 1) % len(names)
        self._load_machine(names[idx])

    # -- Screen protocol -----------------------------------------------------
    def handle_event(self, event):
        if self._menu_requested:
            return "menu"
        for b in self.buttons:
            b.handle_event(event)
        if self._menu_requested:
            return "menu"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self._cycle_machine()
        return None

    def update(self, dt: float) -> None:
        if self.running_auto and self.step_index < len(self.history) - 1:
            self._time_accum += dt
            interval = 1.0 / self.speed
            while self._time_accum >= interval and self.step_index < len(self.history) - 1:
                self.step_index += 1
                self._time_accum -= interval
        else:
            self.running_auto = False

    def draw(self, surface) -> None:
        f = self.fonts
        surface.blit(f["title"].render(self.title, True, COLOR_TEXT), (30, 20))
        surface.blit(
            f["small"].render("Press [M] to cycle example machines | [Esc] back to menu",
                               True, COLOR_MUTED), (30, 60))

        action, config = self.history[self.step_index]
        tape_str = format_tape(config)

        # Tape strip
        pygame.draw.rect(surface, COLOR_PANEL, (30, 110, 940, 90), border_radius=8)
        tape_font = f["mono"]
        max_chars = 70
        display = tape_str
        if len(display) > max_chars:
            display = display[len(display) - max_chars:]
        text_surf = tape_font.render(display, True, COLOR_TEXT)
        surface.blit(text_surf, (50, 150))

        # State / symbol / step info
        info_lines = [
            f"Machine: {self.machine_name}",
            f"Step: {self.step_index} / {len(self.history) - 1}",
            f"State: {config['state']}",
            f"Symbol under head: '{config['symbol']}'",
            f"Action: {action if action else '(running)'}",
        ]
        for i, line in enumerate(info_lines):
            color = COLOR_OK if action == "Accept" else (COLOR_DANGER if action == "Reject" else COLOR_TEXT)
            surface.blit(f["body"].render(line, True, color if i == 4 else COLOR_TEXT), (30, 230 + i * 28))

        status = "RUNNING" if self.running_auto else "PAUSED/STEP MODE"
        surface.blit(f["small"].render(f"Speed: {self.speed} steps/sec   Status: {status}",
                                        True, COLOR_MUTED), (30, 400))

        for b in self.buttons:
            b.draw(surface, f)
