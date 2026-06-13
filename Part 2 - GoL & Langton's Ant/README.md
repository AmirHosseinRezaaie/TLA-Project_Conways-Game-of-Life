<h1>🌱 Part 2: Cellular Automata — Game of Life & Langton’s Ant</h1>

<p><i>From simple local rules to emergent computation and self-organizing systems</i></p>

<hr>

<h2>🧠 Overview</h2>

<p>
This part explores <b>cellular automata</b>, systems where global complexity emerges from simple local rules.
</p>

<p>
It demonstrates how computation can arise naturally from spatial dynamics without any central control.
</p>

<hr>

<h2>🌱 Conway’s Game of Life</h2>

<p>
A zero-player simulation where each cell evolves based on its neighbors.
</p>

<ul>
  <li>Birth, survival, and death rules</li>
  <li>Oscillators, gliders, and moving patterns</li>
  <li>Emergent computational structures</li>
</ul>

<p>
Even with only four rules, the system is capable of universal computation.
</p>

<hr>

<h2>🐜 Langton’s Ant</h2>

<p>
A simple agent moving on a grid that produces highly complex behavior.
</p>

<ul>
  <li>Starts with chaotic random movement</li>
  <li>Eventually forms a repeating “highway” pattern</li>
  <li>Demonstrates emergence of order from randomness</li>
</ul>

<hr>

<h2>🔌 Logic Gates in Game of Life</h2>

<p>
Using gliders as signals, we construct computational logic inside the simulation:
</p>

<ul>
  <li>AND gate using glider collisions</li>
  <li>NOT gate using signal annihilation</li>
  <li>Basis for universal computation</li>
</ul>

<hr>

<h2>📁 Structure</h2>

<pre>
Part 2 - GoL & Langton's Ant/
├── conway.py
├── langton.py
├── langton_pygame.py
├── logic_gates.py
├── pygame_gol.py
├── pygame_viewer.py
└── test_gameoflife_glider.py
</pre>

<hr>

<h2>▶️ Running</h2>

<pre>
python pygame_gol.py
python langton_pygame.py
python test_gameoflife_glider.py
</pre>

<hr>

<h2>🚀 Key Ideas</h2>

<ul>
  <li>Simple local rules generate global complexity</li>
  <li>Computation can emerge from physical-like systems</li>
  <li>Different models of computation are equivalent</li>
  <li>Order can emerge from chaos</li>
</ul>

<hr>

<h2>🧩 Core Insight</h2>

<blockquote>
Computation does not require a computer — it can emerge from the rules of a system itself.
</blockquote>