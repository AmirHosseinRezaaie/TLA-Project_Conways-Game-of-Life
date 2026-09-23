# -*- coding: utf-8 -*-
"""
tla_lab.gui.gol_view
=======================

Conway's Game of Life screen (brief sections 7 & 8): a mouse-driven pattern
editor over the project's own ``GameOfLife`` engine, Play/Pause/Step/Reset/
Clear/Randomize/Speed controls, a Finite/Toroidal boundary toggle (both
already implemented in ``conway.py`` via the ``finite`` flag), and
Load/Save for ``.cells`` files from the shipped Pattern Library.
"""

from __future__ import annotations

import os

import pygame

from tla_lab.gui.app import (
    Screen, Button, COLOR_TEXT, COLOR_MUTED, COLOR_ALIVE, COLOR_DEAD,
    COLOR_GRID_LINE, COLOR_PANEL, COLOR_ACCENT,
)
from tla_lab.core.game_of_life import GameOfLife, GameOfLifeSession, randomize, save_cells
from tla_lab.patterns.library import list_patterns

GRID_N = 60
CELL_PX = 10
GRID_ORIGIN = (30, 100)


class GameOfLifeScreen(Screen):
    title = "Conway's Game of Life"

    def __init__(self, fonts):
        super().__init__(fonts)
        self.finite = False
        self.fast_mode = True
        self.gol = GameOfLife(N=GRID_N, finite=self.finite, fastMode=self.fast_mode)
        self.session = GameOfLifeSession(self.gol)
        self.playing = False
        self.speed = 8  # generations per second
        self._time_accum = 0.0
        self.patterns = [p for p in list_patterns() if p.filepath]
        self.pattern_index = 0
        self._menu_requested = False

        self.buttons = [
            Button((30, 620, 90, 36), "Play", self._play),
            Button((125, 620, 90, 36), "Pause", self._pause),
            Button((220, 620, 80, 36), "Step", self._step),
            Button((305, 620, 80, 36), "Reset", self._reset),
            Button((390, 620, 80, 36), "Clear", self._clear),
            Button((475, 620, 110, 36), "Randomize", self._randomize),
            Button((595, 620, 40, 36), "-", self._slower),
            Button((640, 620, 40, 36), "+", self._faster),
            Button((690, 620, 130, 36), "Toggle Boundary", self._toggle_boundary),
            Button((830, 620, 130, 36), "Back to Menu", self._go_menu),
            Button((30, 660, 130, 30), "Load Pattern", self._load_pattern),
            Button((170, 660, 60, 30), "Prev", self._prev_pattern),
            Button((235, 660, 60, 30), "Next", self._next_pattern),
            Button((305, 660, 130, 30), "Save as .cells", self._save_pattern),
        ]

    # -- controls -----------------------------------------------------------
    def _play(self):
        self.playing = True

    def _pause(self):
        self.playing = False

    def _step(self):
        self.session.step()

    def _reset(self):
        self.session.reset()
        self.playing = False

    def _clear(self):
        self.session.reset()

    def _randomize(self):
        randomize(self.gol, density=0.25)
        self.session.generation = 0
        self.session.population_history = [self.session.population]

    def _slower(self):
        self.speed = max(1, self.speed - 1)

    def _faster(self):
        self.speed = min(60, self.speed + 1)

    def _toggle_boundary(self):
        self.finite = not self.finite
        self.gol.finite = self.finite

    def _prev_pattern(self):
        if self.patterns:
            self.pattern_index = (self.pattern_index - 1) % len(self.patterns)

    def _next_pattern(self):
        if self.patterns:
            self.pattern_index = (self.pattern_index + 1) % len(self.patterns)

    def _load_pattern(self):
        if not self.patterns:
            return
        info = self.patterns[self.pattern_index]
        self.session.reset()
        # Centre-ish placement, clipped by GameOfLife.insertFromFile itself.
        self.gol.insertFromFile(info.filepath, index=(2, 2))
        self.session.population_history = [self.session.population]

    def _save_pattern(self):
        out_dir = os.path.join(os.getcwd(), "saved_patterns")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"gen{self.session.generation}.cells")
        save_cells(self.gol, path, name=f"Saved at generation {self.session.generation}")

    def _go_menu(self):
        self._menu_requested = True

    # -- Screen protocol ------------------------------------------------------
    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        if self._menu_requested:
            return "menu"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
            cell = self._pixel_to_cell(event.pos)
            if cell:
                r, c = cell
                if event.button == 1:
                    self.gol.grid[r, c] = self.gol.aliveValue
                else:
                    self.gol.grid[r, c] = self.gol.deadValue
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            cell = self._pixel_to_cell(event.pos)
            if cell:
                r, c = cell
                self.gol.grid[r, c] = self.gol.aliveValue
        return None

    def _pixel_to_cell(self, pos):
        x, y = pos
        ox, oy = GRID_ORIGIN
        gx, gy = x - ox, y - oy
        if 0 <= gx < GRID_N * CELL_PX and 0 <= gy < GRID_N * CELL_PX:
            return gy // CELL_PX, gx // CELL_PX
        return None

    def update(self, dt: float) -> None:
        if self.playing:
            self._time_accum += dt
            interval = 1.0 / self.speed
            while self._time_accum >= interval:
                self.session.step()
                self._time_accum -= interval

    def draw(self, surface) -> None:
        f = self.fonts
        surface.blit(f["title"].render(self.title, True, COLOR_TEXT), (30, 20))

        # Grid
        ox, oy = GRID_ORIGIN
        grid_px = GRID_N * CELL_PX
        pygame.draw.rect(surface, COLOR_DEAD, (ox, oy, grid_px, grid_px))
        alive_coords = zip(*(self.gol.grid == self.gol.aliveValue).nonzero())
        for r, c in alive_coords:
            pygame.draw.rect(surface, COLOR_ALIVE,
                              (ox + c * CELL_PX, oy + r * CELL_PX, CELL_PX - 1, CELL_PX - 1))
        for i in range(0, GRID_N + 1, 10):
            pygame.draw.line(surface, COLOR_GRID_LINE, (ox + i * CELL_PX, oy), (ox + i * CELL_PX, oy + grid_px))
            pygame.draw.line(surface, COLOR_GRID_LINE, (ox, oy + i * CELL_PX), (ox + grid_px, oy + i * CELL_PX))

        # Side info panel
        panel_x = ox + grid_px + 20
        pygame.draw.rect(surface, COLOR_PANEL, (panel_x, oy, 940 - grid_px - 20, grid_px), border_radius=8)
        lines = [
            f"Generation: {self.session.generation}",
            f"Population: {self.session.population}",
            f"Grid size: {GRID_N} x {GRID_N}",
            f"Boundary: {'Finite' if self.finite else 'Toroidal'}",
            f"Update: {'Fast (vectorised)' if self.fast_mode else 'Normal (loop)'}",
            f"State: {'Playing' if self.playing else 'Paused'}",
            f"Speed: {self.speed} gen/s",
        ]
        for i, line in enumerate(lines):
            surface.blit(f["small"].render(line, True, COLOR_TEXT), (panel_x + 15, oy + 15 + i * 24))

        if self.patterns:
            info = self.patterns[self.pattern_index]
            pat_lines = [
                "Pattern Library:",
                f"{info.name}",
                f"Category: {info.category}",
                f"Size: {info.width}x{info.height}  Pop: {info.population}",
            ]
            for i, line in enumerate(pat_lines):
                surface.blit(f["small"].render(line, True, COLOR_MUTED), (panel_x + 15, oy + 200 + i * 22))

        surface.blit(f["small"].render(
            "Left-click/drag: paint alive cells | Right-click: erase cells",
            True, COLOR_MUTED), (30, oy + grid_px + 10))

        for b in self.buttons:
            b.draw(surface, f)
