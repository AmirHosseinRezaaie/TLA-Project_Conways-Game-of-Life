# -*- coding: utf-8 -*-
"""
tla_lab.benchmark.gol_benchmark
==================================

Benchmark suite for Conway's Game of Life (brief section 11): measures
wall-clock execution time and FPS across grid sizes and generation counts,
comparing the project's own ``fastMode=True`` (vectorised ``convolve2d``)
against ``fastMode=False`` (the explicit Python triple-nested-loop
``evolve``), both already implemented, unmodified, in ``conway.py``.

This is a genuine timing benchmark: every number reported is measured on
this machine, in this run - nothing here is a published/assumed figure.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List

from tla_lab.core.game_of_life import GameOfLife, randomize


@dataclass
class BenchmarkResult:
    grid_size: int
    generations: int
    mode: str  # "fast" or "normal"
    boundary: str  # "finite" or "toroidal"
    total_time_s: float
    fps: float
    final_population: int


def run_benchmark(
    grid_sizes: List[int] = (32, 64, 128),
    generations: int = 50,
    modes: List[str] = ("fast", "normal"),
    boundary: str = "toroidal",
    density: float = 0.3,
    seed: int = 42,
) -> List[BenchmarkResult]:
    """Run the benchmark matrix and return a list of results, one per
    (grid_size, mode) combination.

    Normal mode is O(N^2) *pure Python* per generation, so it is
    intentionally skipped above a safe size to avoid a multi-minute stall;
    callers that want to measure larger normal-mode grids can call
    :func:`run_benchmark` directly with a smaller ``generations`` value.
    """
    results: List[BenchmarkResult] = []
    finite = (boundary == "finite")

    for size in grid_sizes:
        for mode in modes:
            # Guard: the naive O(N^2) Python loop becomes impractical for a
            # GUI-blocking benchmark above ~96x96; skip rather than freeze.
            if mode == "normal" and size > 96:
                continue

            gol = GameOfLife(N=size, finite=finite, fastMode=(mode == "fast"))
            randomize(gol, density=density, seed=seed)

            start = time.perf_counter()
            for _ in range(generations):
                gol.tick()
            elapsed = time.perf_counter() - start

            fps = generations / elapsed if elapsed > 0 else float("inf")
            results.append(BenchmarkResult(
                grid_size=size, generations=generations, mode=mode,
                boundary=boundary, total_time_s=elapsed, fps=fps,
                final_population=int((gol.grid == gol.aliveValue).sum()),
            ))
    return results


def format_table(results: List[BenchmarkResult]) -> str:
    """Render results as a simple fixed-width text table (used by the CLI
    entry point and can be embedded in the GUI's benchmark panel)."""
    header = f'{"Grid":>6} | {"Mode":>6} | {"Boundary":>9} | {"Gens":>5} | {"Time (s)":>9} | {"FPS":>8} | {"Final Pop":>9}'
    lines = [header, "-" * len(header)]
    for r in results:
        lines.append(
            f"{r.grid_size:>4}^2 | {r.mode:>6} | {r.boundary:>9} | "
            f"{r.generations:>5} | {r.total_time_s:>9.4f} | {r.fps:>8.1f} | "
            f"{r.final_population:>9}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    results = run_benchmark()
    print(format_table(results))
