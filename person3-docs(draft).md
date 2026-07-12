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
*Test:* in .\TLA-Project_Conways-Game-of-Life\Part 1 - Busy Beaver\busy_beaver.py, in the last line there is busy_beaver(`n`) call, set `n`=2 and then run `python "Part 1 - Busy Beaver\busy_beaver.py" in the terminal. The result will be:
```
Running Busy Beaver with 2 states.
a: [0]
b: 1[0]
a: [1]1
a: [0]111
b: 1[1]11
Busy beaver finished in 6 steps.
```

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

### Task 3g: Attempt 5-Card Busy Beaver (*continue here*)
*Responsible for:* me.

Try to find or create a 5-state Busy Beaver machine:

- Justify whether your machine is new or explain why it halts
- Compare with known 5-state machines
- Provide reasoning for your design

*Answers*:
- The machine I wrote, althouh isn't extracted from internet, isn't new. It uses a verry simple logic and writes only 8 `1`s and halts in 15 steps, so I can't say it's new, it's simple and known in the sience society. It halts because the machine builds a chain of 1s by bouncing back and forth, and once the chain reaches 8 1s long, it triggers the halt state (h) directly from state e.

- There is a verry huge difference between my BB(5) and the champion BB(5) wich halts in 47,176,870 steps and leaves 4,098 ones.

- I just scaled up the pattern I have used in BB(3) and BB(4) which was sweeping pattern, for BB(5). This way for sure, no world records can be moved, but at least it definitly halts.


### Task 3h: Research and Verify
*Responsible for:* me.

Consult the Busy Beaver Wiki (https://www.sligocki.com/wiki/Busy_Beaver) and study the best known machines:

- Compare 2, 3, and 4-state champion machines
As the number of states increases, the maximum number of steps before halting grows incredibly fast (BB(2)=6, BB(3)=21, BB(4)=107). This illustrates the rapid, non-computable growth of the Busy Beaver function.

- Are your machines better than the known champions? 
Definitely no.

- Implement the champion machines and verify their output
I have implemented the champion transition tables for BB(3) and BB(4) inside `busy_beaver.py`. By running the simulator, I verified that they match the reference limits exactly: the 3-state champion halts in exactly 21 steps, and the 4-state champion halts in exactly 107 steps. right now the champion BBs are commented in the `busy_beaver.py`, in order to tesst it, comment my implemented BBs and un-comment the champion BBs.

- Compare results with your designs
  - **BB(2):** My implementation was mathematically identical to the champion machine, achieving the absolute maximum of 6 steps(Since the instruction was in the main docs).
  - **BB(3):** My design achieved 9 steps (writing five `1`s), while the champion runs for 21 steps (writing six `1`s).
  - **BB(4):** My sweeping pattern achieved 10 steps (writing six `1`s), which is nowhere near the champion's staggering 107 steps (writing thirteen `1`s).
  - **Conclusion:** My designs prioritize predictable, guaranteed-to-halt sweeping patterns. The champion machines rely on highly complex, chaotic behavior to maximize execution time before halting.

**Reference machines locations**:
- 2-card champion: BB(2) = 6
- 3-card champion: BB(3) = 21
- 4-card champion: BB(4) = 107

### Notes:
The given link was broken, working link: https://en.wikipedia.org/wiki/Busy_beaver#Known_values_for_%CE%A3_and_S