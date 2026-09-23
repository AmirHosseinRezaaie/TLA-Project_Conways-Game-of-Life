# -*- coding: utf-8 -*-
"""
tla_lab.gui.busy_beaver_view
===============================

Busy Beaver screen (brief section 6): lets the user pick a state count,
run the project's existing hand-written machine for that count, and see
steps / ones written / halted status. Also exposes the bounded, cancellable
search engine (``tla_lab.core.busy_beaver.BusyBeaverSearch``) for 2-state
machines with a visible progress readout, so a heavy search can never
freeze the UI.
"""

from __future__ import annotations

import threading

import pygame

from tla_lab.gui.app import Screen, Button, COLOR_TEXT, COLOR_MUTED, COLOR_PANEL, COLOR_OK, COLOR_DANGER
from tla_lab.core.busy_beaver import (
    available_state_counts, run_beaver, BusyBeaverSearch, SearchProgress,
)


class BusyBeaverScreen(Screen):
    title = "Busy Beaver"

    def __init__(self, fonts):
        super().__init__(fonts)
        self.available = available_state_counts()
        self.selected_n = self.available[0]
        self.result = None
        self.error = None

        self.search_thread = None
        self.search_engine = None
        self.search_progress: SearchProgress | None = None

        self._menu_requested = False
        self.buttons = [
            Button((30, 100, 40, 36), "<", self._prev_n),
            Button((80, 100, 40, 36), ">", self._next_n),
            Button((150, 100, 140, 36), "Run Machine", self._run_selected),
            Button((30, 620, 220, 40), "Search 2-state (5s)", self._start_search),
            Button((260, 620, 120, 40), "Cancel Search", self._cancel_search),
            Button((780, 620, 190, 40), "Back to Menu", self._go_menu),
        ]

    def _prev_n(self):
        idx = self.available.index(self.selected_n)
        self.selected_n = self.available[(idx - 1) % len(self.available)]

    def _next_n(self):
        idx = self.available.index(self.selected_n)
        self.selected_n = self.available[(idx + 1) % len(self.available)]

    def _run_selected(self):
        try:
            self.result = run_beaver(self.selected_n)
            self.error = None
        except ValueError as e:
            self.result = None
            self.error = str(e)

    def _start_search(self):
        if self.search_thread and self.search_thread.is_alive():
            return  # a search is already running - ignore duplicate clicks
        self.search_engine = BusyBeaverSearch(n_states=2, step_limit=100, timeout_s=5.0)

        def worker():
            self.search_progress = self.search_engine.run(
                on_progress=lambda p: setattr(self, "search_progress", p),
                progress_every=1000,
            )

        self.search_thread = threading.Thread(target=worker, daemon=True)
        self.search_thread.start()

    def _cancel_search(self):
        if self.search_engine:
            self.search_engine.cancel()

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
            "Machines here reproduce the project's own hand-written table "
            "(Part 1/busy_beaver.py). These are demonstration machines, not "
            "claimed as proven optimal Busy Beaver champions.",
            True, COLOR_MUTED), (30, 60))

        surface.blit(f["body"].render(f"States: {self.selected_n}", True, COLOR_TEXT), (30, 150))

        y = 200
        if self.error:
            surface.blit(f["body"].render(self.error, True, COLOR_DANGER), (30, y))
        elif self.result:
            r = self.result
            lines = [
                f"Halted: {r.halted}",
                f"Steps taken: {r.steps}",
                f"Ones written: {r.ones_written}",
                f"Final tape (truncated): {r.tape[:60]}{'...' if len(r.tape) > 60 else ''}",
            ]
            for line in lines:
                surface.blit(f["body"].render(line, True, COLOR_TEXT), (30, y))
                y += 28

        # Search panel
        pygame.draw.rect(surface, COLOR_PANEL, (30, 420, 940, 170), border_radius=8)
        surface.blit(f["heading"].render("Bounded Search (2-state, opt-in)", True, COLOR_TEXT), (45, 435))
        p = self.search_progress
        if p is None:
            surface.blit(f["small"].render("No search run yet.", True, COLOR_MUTED), (45, 470))
        else:
            status = "cancelled" if p.cancelled else ("timed out" if p.timed_out else "finished")
            lines = [
                f"Machines tried: {p.machines_tried}    Status: {status}    "
                f"Elapsed: {p.elapsed_seconds:.2f}s",
                f"Best halting machine found: {p.best_ones} ones in {p.best_steps} steps"
                if p.best_ones >= 0 else "No halting machine found yet.",
            ]
            for i, line in enumerate(lines):
                surface.blit(f["small"].render(line, True, COLOR_TEXT), (45, 470 + i * 24))

        for b in self.buttons:
            b.draw(surface, f)
