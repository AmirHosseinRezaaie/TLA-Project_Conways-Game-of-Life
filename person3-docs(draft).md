Person3 = AminEslamian
Note: This document is draft only and will be implemented into the main docs later.

---

# **Documents and Explanations:**

## Part 1 - Section 3

### Task 3a: Understanding Undecidability
*Responsible for:* me
**Question:** Explain why finding Busy Beaver machines is difficult and why the problem is undecidable.
Key points to address:
- Connection to the Halting Problem
- Why brute force search becomes computationally infeasible
- What makes this problem fundamentally non-computable


**Explanation:** *FILL HERE*

### Task 3b - Implement Two-Way Infinite Tape
(Modify turing_machine.py)
*Responsible for:* not me.

### Task 3c - Why Use Generators?
*Responsible for:* ??
Explain the benefits of using Python generators in Turing machine simulation.
Considerations:
- Memory efficiency for long computations
- Interactivity and step-by-step debugging
- Suspension and resumption of computation
- Streaming output without storing entire history

### Task 3d: Run 2-Card Busy Beaver
*Responsible for:* me.

The BB(2) was implemented as instructured.
*Quetion:* Starting with a blank tape, how many 1s does the machine produce?
*Answer:* four `1`s (Was tested).

### Task 3e: Compare with Known Results
*Responsible for:* me

Compare your result with the best known 2-state machines from the Busy Beaver Wiki:

- Is your output correct?
Yes, the output is correct. The machine successfully halts, leaving exactly four 1s on the tape and taking 6 steps to complete the computation.
Output:
`
Running Busy Beaver with 2 states.
a: [0]
b: 1[0]
a: [1]1
a: [0]111
b: 1[1]11
Busy beaver finished in 6 steps.
`
- How does it compare to the optimal 2-state machine?
It is completely identical! The given instructure for the BB(2) in the docs is exactly the same as the trophy BB(2).
- Evaluate your result against established benchmarks
Since the provided machine is mathematically equivalent to the known benchmark champion for BB(2), my result perfectly matches the absolute upper limit of computation possible for a 2-state Turing machine. No 2-state machine can produce more than four 1s or run for more than 6 steps and still halt.

### Task 3f: Create 3 and 4-Card Busy Beaver Machines
*Responsible for:*  me.

Design and implement your own Busy Beaver machines with 3 and 4 states:

- You do not need to find the absolute optimal machines (BB(3) and BB(4))
- Just create machines that outperform the 2-state machines
- Show the number of 1s produced by each machine
Our own editon of BB(3) and BB(4) was implemented. The numbers of `1`s produced and number of steps each took, is commented next to them in the busy_beaver.py.
For BB(3): 9 steps and 5 `1`s.
For BB(4): 10 steps and 6 `1`s.

### Task 3g: Attempt 5-Card Busy Beaver
*Responsible for:* me.

Try to find or create a 5-state Busy Beaver machine:

- Justify whether your machine is new or explain why it halts
- Compare with known 5-state machines
- Provide reasoning for your design

### Task 3h: Research and Verify
*Responsible for:* me.

Consult the Busy Beaver Wiki (https://www.sligocki.com/wiki/Busy_Beaver) and study the best known machines:

- Compare 2, 3, and 4-state champion machines
- Are your machines better than the known champions? 
Definitly no.
- Implement the champion machines and verify their output
- Compare results with your designs

**Reference machines locations**:
- 2-card champion: BB(2) = 6
- 3-card champion: BB(3) = 21
- 4-card champion: BB(4) = 107
