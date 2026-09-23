# -*- coding: utf-8 -*-
"""
tla_lab.gui.langton_view
===========================

Langton's Ant screen (brief section 10): rule selection (RL, LLRR,
LRRRRLL, ... ) or a typed custom rule, live grid + ant visualization on top
of the unmodified ``LangtonsAnt`` class, and statistics (steps, position,
direction, cells visited, bounding box, black/white cell counts) computed
by ``tla_lab.core.langtons_ant.AntAnalyzer``.
"""

from __future__ import annotations

import pygame

from tla_lab.gui.app import (
    Screen, Button, COLOR_TEXT, COLOR_MUTED, COLOR_ALIVE, COLOR_DEAD,
    COLOR_ACCENT, COLOR_PANEL, COLOR_GRID_LINE, COLOR_DANGER,
)
from tla_lab.core.langtons_ant import LangtonsAnt, parse_rule_string, AntAnalyzer, KNOWN_RULES

GRID_N = 90
CELL_PX = 6
GRID_ORIGIN = (30, 100)

DIRECTION_NAMES = {0: "North", 1: "East", 2: "South", 3: "West"}


class LangtonAntScreen(Screen):
    title = "Langton's Ant"

    def __init__(self, fonts):
        super().__init__(fonts)
        self.rule_names = list(KNOWN_RULES.keys())
        self.rule_index = 0
        self.custom_rule_text = ""
        self.editing_custom = False
        self.error = None
        self.playing = False
        self.speed = 30
        self._time_accum = 0.0
        self._menu_requested = False
        self._new_ant(KNOWN_RULES[self.rule_names[0]])

        self.buttons = [
            Button((30, 620, 90, 36), "Play", self._play),
            Button((125, 620, 90, 36), "Pause", self._pause),
            Button((220, 620, 80, 36), "Step", self._step),
            Button((305, 620, 80, 36), "Reset", self._reset),
            Button((395, 620, 40, 36), "-", self._slower),
            Button((440, 620, 40, 36), "+", self._faster),
            Button((490, 620, 150, 36), "Next Known Rule", self._next_rule),
            Button((650, 620, 150, 36), "Edit Custom Rule", self._toggle_custom_edit),
            Button((830, 620, 130, 36), "Back to Menu", self._go_menu),
        ]

    def _new_ant(self, rule_string: str):
        try:
            rules = parse_rule_string(rule_string)
        except ValueError as e:
            self.error = str(e)
            return
        self.error = None
        self.rule_string = rule_string
        self.ant = LangtonsAnt(N=GRID_N, ant_position=(GRID_N // 2, GRID_N // 2), rules=rules)
        self.analyzer = AntAnalyzer(self.ant, rule_string=rule_string)

    def _play(self):
        self.playing = True

    def _pause(self):
        self.playing = False

    def _step(self):
        self.analyzer.step()

    def _reset(self):
        self._new_ant(self.rule_string)
        self.playing = False

    def _slower(self):
        self.speed = max(1, self.speed - 5)

    def _faster(self):
        self.speed = min(500, self.speed + 5)

    def _next_rule(self):
        self.editing_custom = False
        self.rule_index = (self.rule_index + 1) % len(self.rule_names)
        self._new_ant(KNOWN_RULES[self.rule_names[self.rule_index]])
        self.playing = False

    def _toggle_custom_edit(self):
        self.editing_custom = not self.editing_custom

    def _go_menu(self):
        self._menu_requested = True

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        if self._menu_requested:
            return "menu"

        if self.editing_custom and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._new_ant(self.custom_rule_text)
                self.editing_custom = False
            elif event.key == pygame.K_BACKSPACE:
                self.custom_rule_text = self.custom_rule_text[:-1]
            elif event.unicode.upper() in ("L", "R"):
                self.custom_rule_text += event.unicode.upper()
        return None

    def update(self, dt: float) -> None:
        if self.playing and not self.error:
            self._time_accum += dt
            interval = 1.0 / self.speed
            while self._time_accum >= interval:
                self.analyzer.step()
                self._time_accum -= interval

    def draw(self, surface) -> None:
        f = self.fonts
        surface.blit(f["title"].render(self.title, True, COLOR_TEXT), (30, 20))

        ox, oy = GRID_ORIGIN
        grid_px = GRID_N * CELL_PX
        pygame.draw.rect(surface, COLOR_DEAD, (ox, oy, grid_px, grid_px))

        if not self.error:
            colored = (self.ant.grid != 0).nonzero()
            for r, c in zip(*colored):
                pygame.draw.rect(surface, COLOR_ALIVE,
                                  (ox + int(c) * CELL_PX, oy + int(r) * CELL_PX, CELL_PX, CELL_PX))
            ar, ac = self.ant.get_current_position()
            pygame.draw.rect(surface, COLOR_ACCENT,
                              (ox + ac * CELL_PX - 1, oy + ar * CELL_PX - 1, CELL_PX + 2, CELL_PX + 2))

        panel_x = ox + grid_px + 20
        pygame.draw.rect(surface, COLOR_PANEL, (panel_x, oy, 940 - grid_px - 20, grid_px), border_radius=8)

        if self.error:
            surface.blit(f["small"].render("Invalid rule:", True, COLOR_DANGER), (panel_x + 15, oy + 15))
            surface.blit(f["small"].render(self.error, True, COLOR_DANGER), (panel_x + 15, oy + 40))
        else:
            r, c = self.ant.get_current_position()
            bbox = self.analyzer.bounding_box
            counts = self.analyzer.color_counts()
            lines = [
                f"Rule: {self.rule_string}",
                f"Steps: {self.analyzer.steps_taken}",
                f"Position: ({r}, {c})",
                f"Direction: {DIRECTION_NAMES[self.ant.direction]}",
                f"Turns L/R: {self.analyzer.turns_left}/{self.analyzer.turns_right}",
                f"Cells visited: {self.analyzer.cells_visited}",
                f"Bounding box: {bbox}",
                f"Colour counts: {counts}",
                f"Highway-like: {self.analyzer.looks_like_highway()}",
            ]
            for i, line in enumerate(lines):
                surface.blit(f["small"].render(line[:60], True, COLOR_TEXT), (panel_x + 15, oy + 15 + i * 24))

        # Custom rule editor box
        box_color = COLOR_ACCENT if self.editing_custom else COLOR_MUTED
        pygame.draw.rect(surface, COLOR_PANEL, (30, oy + grid_px + 10, 400, 30), border_radius=4)
        pygame.draw.rect(surface, box_color, (30, oy + grid_px + 10, 400, 30), width=1, border_radius=4)
        hint = "Type L/R, Enter to apply" if self.editing_custom else "Click 'Edit Custom Rule' to type L/R sequence"
        text = self.custom_rule_text if self.editing_custom else hint
        surface.blit(f["small"].render(text, True, COLOR_TEXT if self.editing_custom else COLOR_MUTED),
                     (40, oy + grid_px + 17))

        for b in self.buttons:
            b.draw(surface, f)
