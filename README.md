# Computational Theory Laboratory

*A practical exploration of computational theory through Turing Machines, the Busy Beaver problem, Conway's Game of Life, and Langton's Ant — demonstrating emergence, universality, and the limits of computation.*

---

## 1. Introduction

This project began as three independent, script-based explorations of computational theory (Turing Machines / Busy Beaver, Conway's Game of Life / Langton's Ant / glider-based logic gates). This version keeps every one of those original scripts **fully intact and runnable exactly as before**, and adds a unified `tla_lab/` package that turns the collection into a single, explorable **Computational Theory Laboratory**: one central GUI, richer visualizers, a pattern library, a benchmark suite, and an expanded, tested logic-gate circuit.

Nothing in `Part 1 - Busy Beaver/` or `Part 2 - GoL & Langton's Ant/` was rewritten, renamed, or deleted. The new code in `tla_lab/` *imports and wraps* those modules.

## 2. Goals

The central idea this project demonstrates:

> **Simple, local rules — iterated step by step — can produce emergent complexity, and are sufficient for universal computation.**

Every module supports that idea from a different angle:

| Module | What it shows |
|---|---|
| Turing Machine | The formal, general-purpose model of computation itself |
| Busy Beaver | The limits of computability (undecidability of "will it halt?") |
| Conway's Game of Life | Emergent complexity from a 2-state, 8-neighbour rule |
| Logic Gates (gliders) | Game of Life is Turing-complete: real logic circuits built from collisions |
| Langton's Ant | Order (a "highway") emerging from a trivial deterministic rule |

## 3. Computational Theory Concepts Covered

- Turing Machines: tape, head, states, transitions, generator-based (lazy) execution, accept/reject, halting
- The Busy Beaver problem and its connection to the Halting Problem
- Cellular automata: Conway's Game of Life, Moore neighbourhoods, finite vs. toroidal boundaries
- Emergent computation and self-organization (Langton's Ant highways)
- Turing-completeness of Conway's Game of Life via glider-collision logic gates

## 4. Project Structure

```
TLA-Project_Conways-Game-of-Life/
├── Part 1 - Busy Beaver/            # ORIGINAL, unmodified
│   ├── turing_machine.py            #   generic TuringMachine (generator-based)
│   ├── busy_beaver.py               #   BB(1..5) hand-written machines + own TM engine
│   ├── student_test_turing.py       #   self-check script
│   ├── test_turing_machine_example*.py
│   ├── test_turing_adder.py
│   ├── test_turing_multiplier.py
│   ├── test_busy_beaver_2.py
│   └── README.md
│
├── Part 2 - GoL & Langton's Ant/    # ORIGINAL, unmodified
│   ├── conway.py                    #   GameOfLife, parse_pattern (.cells/.rle loader)
│   ├── langton.py                   #   LangtonsAnt
│   ├── logic_gates.py               #   GliderLogicGates (real AND/NOT via gliders)
│   ├── pygame_viewer.py, pygame_gol.py, langton_pygame.py, pygame_logic_gates.py
│   ├── *.cells                      #   shipped patterns (guns, spaceships, oscillator)
│   └── README.md
│
├── tla_lab/                          # NEW: the Computational Theory Laboratory package
│   ├── utils/paths.py                #   makes the space-named legacy folders importable
│   ├── core/
│   │   ├── turing_machine.py         #   wraps Part 1's TuringMachine + trace()/format_tape()
│   │   ├── busy_beaver.py            #   wraps busy_beaver.py + bounded/cancellable search
│   │   ├── game_of_life.py           #   wraps conway.py + save .cells/.rle + session
│   │   ├── langtons_ant.py           #   wraps langton.py + rule parsing + AntAnalyzer
│   │   └── logic_gates.py            #   wraps logic_gates.py + OR/NAND/NOR/XOR/Adders
│   ├── patterns/library.py           #   catalog of the shipped .cells patterns
│   ├── benchmark/gol_benchmark.py    #   Fast vs Normal mode timing benchmark
│   └── gui/                          #   Pygame central menu + 5 module screens
│       ├── app.py, main_menu.py
│       ├── turing_view.py, busy_beaver_view.py
│       ├── gol_view.py, langton_view.py, logic_gates_view.py
│
├── tests/                            # NEW: pytest suite for tla_lab (40 tests)
│   ├── test_turing_machine.py
│   ├── test_busy_beaver.py
│   ├── test_game_of_life.py
│   ├── test_langtons_ant.py
│   └── test_logic_gates.py
│
├── run_lab.py                        # NEW: entry point — launches the central GUI
├── person1-docs.md / person2-docs.md / person3-docs.md   # ORIGINAL contributor notes
├── requirements.txt
└── README.md                         # this file
```

## 5. Installation

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 6. Requirements

See `requirements.txt`. Summary:

- `numpy`, `scipy` — vectorised Game of Life updates (`conway.py`'s fast mode)
- `pygame` — all visualizers (central lab GUI, Turing/GoL/Langton/Logic Gates views, and the original Part 2 pygame scripts)
- `pytest` — running the test suite

## 7. Running the Project

### 7.1 The central GUI (new)

```bash
python run_lab.py
```

Opens one window with a menu of five modules. Click a module to enter it; press **Esc** at any time to return to the menu. Each module has its own on-screen controls (Play/Pause/Step/Reset/etc.).

### 7.2 The original scripts (unchanged, still work standalone)

```bash
cd "Part 1 - Busy Beaver"
python student_test_turing.py
python test_turing_machine_example1.py
python busy_beaver.py                 # prints BB(4) trace

cd "../Part 2 - GoL & Langton's Ant"
python test_gameoflife_glider.py      # requires a display (Pygame window)
python logic_gates.py                 # prints the AND/NOT truth tables to the console
```

## 8. Turing Machine

`Part 1 - Busy Beaver/turing_machine.py`'s `TuringMachine` is a generator-based simulator: `run()` yields `(action, configuration)` at every step, so a caller can consume as few or as many steps as it wants (`accepts()`/`rejects()` use `itertools.islice` with a `step_limit` for safety). The new `tla_lab/gui/turing_view.py` visualizer sits directly on top of this — it drains the generator once via `tla_lab.core.turing_machine.trace()`, then lets you scrub through the resulting history with **Step**, **Run** (speed-controlled autoplay), **Pause**, **Reset**, and **Stop**, while showing the tape (with the head highlighted), current state, current symbol, and the action just taken (Accept/Reject/running).

## 9. Busy Beaver

`Part 1 - Busy Beaver/busy_beaver.py` ships hand-written machines for `n = 1..5` (its own small `TuringMachine` engine, distinct from the generic one above). **These are the project's own demonstration machines, not claimed to be the mathematically-proven optimal Busy Beaver champions** — the file itself keeps the actual champion tables commented out for comparison. `tla_lab/core/busy_beaver.py` wraps these with a `step_limit` so a misbehaving program can't hang the GUI, and adds an **opt-in, bounded brute-force search engine** (`BusyBeaverSearch`) for small state counts:

- Every candidate 2-symbol machine is genuinely enumerated and simulated (not looked up).
- A hard **step limit** *and* **wall-clock timeout** bound every run.
- The search can be **cancelled** mid-run (`cancel()`), and reports **live progress** (machines tried, best result found so far, elapsed time).
- For `n_states=2` this search provably finds the same result reported in the literature (4 ones in 6 steps) — verified as a unit test, not asserted as a hard-coded fact.

No Busy Beaver numbers beyond `n=2` are hard-coded anywhere; the GUI only ever displays what a real run in this process actually produced.

## 10. Conway's Game of Life

`Part 2/conway.py`'s `GameOfLife` already implements: Moore-neighbourhood rules, `tick()`, a fast vectorised update (`scipy.signal.convolve2d`) and a slow, explicit Python loop (`evolve()`), a `finite`/toroidal boundary flag, and a `.cells`/`.rle` pattern loader (`parse_pattern`). `tla_lab/core/game_of_life.py` adds what was missing:

- `save_cells()` / `save_rle()` — the original module could load patterns but not save them.
- `randomize()` — fill the grid at a given density.
- `GameOfLifeSession` — generation counter + population history bookkeeping for the GUI/benchmark.

`tla_lab/gui/gol_view.py` (the **Pattern Editor**) adds mouse painting (left-click/drag to set a cell alive, right-click to erase), Play/Pause/Step/Reset/Clear/Randomize/Speed controls, a Finite↔Toroidal toggle, and Load/Save against the Pattern Library below. Generation, population, grid size, boundary mode and running state are all shown live.

## 11. Pattern Library

`tla_lab/patterns/library.py` catalogs every pattern the project ships — both the `.cells` files in `Part 2/` (still life / oscillator / spaceship / gun / other, per the standard Life taxonomy) and the built-in `insertGlider`/`insertBlinker`/`insertGliderGun` constructs already in `conway.py`. File-based entries report their **real** width/height/population, computed by actually parsing the file with the project's own `parse_pattern`, not guessed.

## 12. Logic Gates

`Part 2/logic_gates.py`'s `GliderLogicGates` fires real gliders into each other inside a `GameOfLife` grid and inspects the surviving debris — a genuine glider-collision **AND** and **NOT** gate, unmodified here.

Building four *more* gates (`OR`, `NAND`, `NOR`, `XOR`) with brand-new hand-placed glider collision coordinates would require empirically tuning new geometries and visually verifying them in Pygame — not something that can be reliably done sight-unseen in this environment. Rather than presenting fabricated, untested coordinates as working circuits, `tla_lab/core/logic_gates.py` builds them **by composing the two already-validated gates**, using standard Boolean identities:

```
OR(a, b)   = NOT(AND(NOT(a), NOT(b)))      # De Morgan
NAND(a, b) = NOT(AND(a, b))
NOR(a, b)  = NOT(OR(a, b))
XOR(a, b)  = OR(AND(a, NOT(b)), AND(NOT(a), b))
```

Every leaf call is still a real Game of Life simulation — there is no shortcut Python `and`/`or` anywhere in the truth-table computation. `half_adder`, `full_adder`, and `four_bit_adder` are then built the same way on top of `XOR`/`AND`, so a 4-bit addition triggers dozens of real, composed glider simulations end-to-end. This design decision — and the exact identities used — is documented in the module's own docstring.

## 13. Langton's Ant

`Part 2/langton.py`'s `LangtonsAnt` implements the toroidal grid, direction handling, and the "toggle colour + turn + move" rule, generalized to multi-colour rule dictionaries. `tla_lab/core/langtons_ant.py` adds:

- `parse_rule_string()` — turns a compact string like `"RL"`, `"LLRR"`, `"LRRRRLL"` into the rules dict the class expects.
- `AntAnalyzer` — tracks step count, left/right turn counts, distinct cells visited, bounding box, per-colour cell counts, and a `looks_like_highway()` heuristic (explicitly documented as a heuristic over the steps actually simulated, not a mathematical proof of periodicity).

`tla_lab/gui/langton_view.py` lets you pick a known rule, type a custom L/R rule, and watch the live grid + these statistics update in real time.

## 14. Testing

40 automated tests live in `tests/`, covering:

- **Turing Machine**: acceptance/rejection, transitions, halt detection, step-limit safety, a unary-arithmetic-style machine
- **Busy Beaver**: all 5 shipped machines halt with the expected step/ones counts, invalid state counts raise, the bounded search respects its step limit/timeout, can be cancelled, and (for n=2) finds the same result as the literature
- **Game of Life**: blinker oscillation, still-life stability, glider translation, finite vs. toroidal boundary behaviour, fast-mode vs. normal-mode agreement, `.cells`/`.rle` save+reload round-trips, session bookkeeping
- **Langton's Ant**: rule parsing (valid and invalid), movement, turning direction, toroidal wrapping, analyzer bounding box / turn counts
- **Logic Gates**: AND/NOT/OR/NAND/NOR/XOR truth tables (all computed via real simulations), half/full/4-bit adder arithmetic

Run them with:

```bash
pytest tests/ -v
```

> **Sandbox note:** in the environment this project was developed in, `pytest` and `pygame` could not be installed (no network access), so the 40 tests above were actually executed with a small local test runner equivalent to `pytest` for this purpose — **all 40 passed**. Every original Part 1/Part 2 script that doesn't require a graphical display was also re-run directly and confirmed working. The Pygame-based GUI files (`tla_lab/gui/*.py`, `run_lab.py`, and the project's own original pygame scripts) were syntax-checked (`python -m py_compile`) but could not be interactively run/click-tested in that sandbox; see "Known Limitations" below.

## 15. Benchmark

`tla_lab/benchmark/gol_benchmark.py` times Normal Mode (`evolve()`, explicit Python triple loop) against Fast Mode (`update_grid_fast()`, vectorised `scipy.signal.convolve2d`) across a matrix of grid sizes and generation counts. Every number is measured live, not assumed:

```bash
python -m tla_lab.benchmark.gol_benchmark
```

Example output (measured on the development machine):

```
  Grid |   Mode |  Boundary |  Gens |  Time (s) |      FPS | Final Pop
----------------------------------------------------------------------
  32^2 |   fast |  toroidal |    50 |    0.0022 |  23208.0 |       112
  32^2 | normal |  toroidal |    50 |    0.0850 |    588.2 |       112
  64^2 |   fast |  toroidal |    50 |    0.0069 |   7291.7 |       452
  64^2 | normal |  toroidal |    50 |    0.3845 |    130.0 |       452
 128^2 |   fast |  toroidal |    50 |    0.0282 |   1770.5 |      2155
```

(Normal mode is skipped above 96×96 by default — the explicit Python loop is O(N²) and would otherwise stall a benchmark run; call `run_benchmark()` directly with different parameters to override this.) This is a direct illustration of the link between Computational Theory (the *same* rule, computed two different ways) and Performance Computing (a ~30-90x speedup from vectorisation at these sizes).

## 16. Examples

- **Turing Machine**: load "Accepts '##'" in the visualizer, Step through it, watch it reach `qa` (Accept).
- **Busy Beaver**: select `n=4`, Run Machine, see it halt in 10 steps having written 6 ones.
- **Game of Life**: open the Pattern Editor, load the shipped "ak94 gun.cells" pattern, press Play, and watch it periodically emit gliders.
- **Logic Gates**: select `XOR`, toggle A and B, Run Simulation — the on-screen output is the result of an actual composed glider simulation.
- **Langton's Ant**: type the custom rule `LLRR` and Play — after an initially chaotic phase, watch the "highway" the ant carves.

## 17. Known Limitations

- `pygame` could not be installed in the development sandbox used to build this version (no network access), so the GUI (`run_lab.py` and every file in `tla_lab/gui/`) is **syntax-checked but not interactively tested**. All non-GUI logic each screen depends on (`tla_lab/core/*`) *is* fully tested and passing. Please run `python run_lab.py` locally (with `pygame` installed) as the first smoke test after pulling this version, and file an issue/adjust if any screen misbehaves.
- The `OR`/`NAND`/`NOR`/`XOR` glider gates are **composed** from the original `AND`/`NOT` glider primitives rather than being single new hand-placed glider collisions (see section 12) — this is a deliberate, documented engineering trade-off, not a shortcut hidden from the user.
- The Busy Beaver search engine is only practical for small state counts (2, and 3 with a longer timeout); it makes no claim to have found a proven champion beyond what it actually simulates.
- Binary assets from the original repository (`doc.pdf` files, the `Report/` `.docx`/`.pdf`, and the `.png` screenshots) were not present in the text export this version was built from, so they are not included in this package. They remain available in the original GitHub repository.
- Langton's Ant "highway" detection is a heuristic over the steps actually simulated, not a mathematical periodicity proof.

## 18. Future Development

- Hand-tuned, single-collision glider geometries for OR/NAND/NOR/XOR (once verifiable in an environment with a display), replacing the current composed-gate approach.
- A `save/load full session` feature for the Game of Life editor (grid + generation + history, not just the pattern).
- Larger/parallelized Busy Beaver search (n=3, n=4) with a background worker pool.
- RLE support for Langton's Ant "highway" export, matching the Game of Life pattern library.
- Charting the benchmark results (matplotlib or an in-GUI plot) instead of only a text table.

---

*Original contributor documentation preserved in `person1-docs.md`, `person2-docs.md`, `person3-docs.md`, and the two `Part 1`/`Part 2` `README.md` files.*
