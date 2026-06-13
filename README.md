<h1>Theory of Languages and Automata - Practical Project</h1>

<p><i>A computational exploration of Turing Machines and Cellular Automata</i></p>

<hr>

<h2>🧠 Overview</h2>

<p>
This project implements core concepts from <b>Theory of Computation</b>, focusing on how computation emerges from simple formal systems.
</p>

<p>
It demonstrates both the <b>power and limits of computation</b> using classical theoretical models.
</p>

<ul>
  <li>Turing Machines as a universal model of computation</li>
  <li>Busy Beaver problem and undecidability</li>
  <li>Conway’s Game of Life and emergent computation</li>
  <li>Langton’s Ant as a chaotic deterministic system</li>
  <li>Construction of logic gates using cellular automata</li>
</ul>

<hr>

<h2>🌱 Conway’s Game of Life</h2>

<img src="https://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif" width="520">

<p>
A zero-player game where simple local rules generate highly complex global behavior.  
Patterns such as gliders and oscillators demonstrate computational universality.
</p>

<br>

<h2>🐜 Langton’s Ant</h2>

<img src="https://upload.wikimedia.org/wikipedia/commons/0/09/LangtonsAntAnimated.gif" width="520">

<p>
A simple agent-based system that evolves from chaotic motion into structured highways, illustrating emergence of order from randomness.
</p>

<hr>

<h2>📁 Project Structure</h2>

<pre>
Part 1 - Busy Beaver/
    Turing Machine simulator
    Unary arithmetic (add, multiply)
    Busy Beaver exploration

Part 2 - GoL & Langton's Ant/
    Conway’s Game of Life
    Langton’s Ant
    Logic gates using gliders
</pre>

<hr>

<h2>⚙️ Installation</h2>

<pre>
pip install -r requirements.txt
</pre>

<hr>

<h2>▶️ Running Tests</h2>

<p><b>Turing Machines:</b></p>
<pre>
python test_turing_machine_example1.py
</pre>

<p><b>Game of Life:</b></p>
<pre>
python test_gameoflife_glider.py
</pre>

<hr>

<h2>🚀 What This Project Demonstrates</h2>

<ul>
  <li>Computation can be modeled using abstract machines</li>
  <li>Universality of Turing Machines</li>
  <li>Emergence of complexity from simple rules</li>
  <li>Equivalence of different computational models</li>
  <li>Physical interpretation of computation via patterns and signals</li>
</ul>

<hr>

<h2>🧩 Key Idea</h2>

<blockquote>
Simple rules, when iterated, can generate universal computation.
</blockquote>

<hr>

<h2>📌 Notes</h2>

<p>
Each subsystem is independently executable and designed for educational exploration of computation theory.
</p>