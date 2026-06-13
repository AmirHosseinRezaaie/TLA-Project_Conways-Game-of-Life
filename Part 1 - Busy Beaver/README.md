<h1>🧮 Part 1: Turing Machines and the Busy Beaver Problem</h1>

<p><i>Exploring the foundations of computation through machines, symbols, and undecidability</i></p>

<hr>

<h2>🧠 Overview</h2>

<p>
This part implements a complete <b>Turing Machine simulator</b> and uses it as a tool to explore the limits of computation.
</p>

<p>
Despite its simple definition, a Turing Machine can simulate any algorithm — making it the foundation of modern computer science.
</p>

<hr>

<h2>⚙️ What This Part Includes</h2>

<ul>
  <li>Full Turing Machine simulator (generator-based execution)</li>
  <li>One-way and two-way infinite tape support</li>
  <li>Unary arithmetic (addition and multiplication)</li>
  <li>Step-by-step debugging and visualization tools</li>
  <li>Busy Beaver exploration (maximizing halting output)</li>
</ul>

<hr>

<h2>🧮 Unary Computation</h2>

<p>
Numbers are represented using unary encoding (e.g., 3 = 111).  
This allows arithmetic operations to be performed purely through symbol rewriting.
</p>

<ul>
  <li>Addition: merging unary sequences</li>
  <li>Multiplication: repeated concatenation</li>
</ul>

<hr>

<h2>🔥 Busy Beaver Problem</h2>

<p>
The Busy Beaver function explores the limits of computation by asking:
</p>

<blockquote>
“What is the maximum number of 1s a halting Turing Machine can produce?”
</blockquote>

<p>
This problem is deeply connected to the <b>Halting Problem</b> and is known to be non-computable.
</p>

<hr>

<h2>📁 Structure</h2>

<pre>
Part 1 - Busy Beaver/
├── turing_machine.py
├── busy_beaver.py
├── student_test_turing.py
├── test_turing_adder.py
├── test_turing_multiplier.py
└── test_busy_beaver_2.py
</pre>

<hr>

<h2>▶️ Running Tests</h2>

<pre>
python test_turing_machine_example1.py
python test_turing_adder.py
python test_busy_beaver_2.py
</pre>

<hr>

<h2>🚀 Key Ideas</h2>

<ul>
  <li>Turing Machines define the limits of computability</li>
  <li>Simple rules can encode all computation</li>
  <li>Some problems are fundamentally undecidable</li>
  <li>Computation can be step-by-step and symbolic</li>
</ul>

<hr>

<h2>🧩 Core Insight</h2>

<blockquote>
A simple symbolic system is enough to represent all possible computation — and also its limits.
</blockquote>