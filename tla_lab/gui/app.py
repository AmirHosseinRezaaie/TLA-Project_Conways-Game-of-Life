# -*- coding: utf-8 -*-
"""
tla_lab.gui.app
==================

A small, dependency-free-beyond-Pygame application shell shared by the
central menu and all five feature views (Turing Machine, Busy Beaver,
Game of Life, Langton's Ant, Logic Gates). Kept intentionally simple - no
GUI framework beyond Pygame itself, per brief section 4 ("avoid heavy
unnecessary frameworks").

Every view is a small class implementing:

    handle_event(event) -> Optional[str]   # return "menu" to go back
    update(dt: float) -> None
    draw(surface) -> None

so :class:`App` can drive any of them identically.
"""

from __future__ import annotations

import pygame

# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

WINDOW_SIZE = (1000, 700)
FPS = 60

COLOR_BG = (18, 18, 24)
COLOR_PANEL = (30, 30, 38)
COLOR_TEXT = (230, 230, 235)
COLOR_MUTED = (150, 150, 160)
COLOR_ACCENT = (80, 170, 255)
COLOR_ALIVE = (240, 240, 245)
COLOR_DEAD = (35, 35, 42)
COLOR_GRID_LINE = (50, 50, 58)
COLOR_BUTTON = (45, 45, 56)
COLOR_BUTTON_HOVER = (60, 60, 74)
COLOR_DANGER = (220, 90, 90)
COLOR_OK = (90, 200, 130)


def get_fonts():
    pygame.font.init()
    return {
        "title": pygame.font.SysFont("consolas,menlo,monospace", 34, bold=True),
        "heading": pygame.font.SysFont("consolas,menlo,monospace", 22, bold=True),
        "body": pygame.font.SysFont("consolas,menlo,monospace", 16),
        "mono": pygame.font.SysFont("consolas,menlo,monospace", 15),
        "small": pygame.font.SysFont("consolas,menlo,monospace", 13),
    }


class Button:
    """A minimal clickable rectangle with a label. No external UI toolkit."""

    def __init__(self, rect, label, on_click=None, enabled=True):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.enabled = enabled
        self.hovered = False

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.on_click:
                self.on_click()

    def draw(self, surface, fonts):
        color = COLOR_BUTTON_HOVER if (self.hovered and self.enabled) else COLOR_BUTTON
        if not self.enabled:
            color = (35, 35, 40)
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_ACCENT if self.hovered and self.enabled else COLOR_GRID_LINE,
                          self.rect, width=1, border_radius=6)
        text_color = COLOR_TEXT if self.enabled else COLOR_MUTED
        text = fonts["body"].render(self.label, True, text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))


class Screen:
    """Base class every feature view inherits from."""

    title = "Screen"

    def __init__(self, fonts):
        self.fonts = fonts

    def handle_event(self, event):
        return None

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: "pygame.Surface") -> None:
        pass


class App:
    """Drives a stack-less single-active-screen application: the central
    menu is screen 0; selecting a module swaps in that module's Screen and
    a "Back to Menu" affordance (ESC key, or each screen's own back button)
    swaps back.
    """

    def __init__(self, menu_screen_factory, title="Computational Theory Laboratory"):
        pygame.init()
        pygame.display.set_caption(title)
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.fonts = get_fonts()
        self.menu_screen_factory = menu_screen_factory
        self.current = menu_screen_factory(self.fonts)
        self.running = True

    def go_to_menu(self):
        self.current = self.menu_screen_factory(self.fonts)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.go_to_menu()
                    continue
                result = self.current.handle_event(event)
                if result == "menu":
                    self.go_to_menu()
            self.current.update(dt)
            self.surface.fill(COLOR_BG)
            self.current.draw(self.surface)
            pygame.display.flip()
        pygame.quit()
