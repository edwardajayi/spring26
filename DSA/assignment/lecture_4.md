
# Lecture 4: Recursion, Complexity, and Intractable Problems

## Introduction
This lecture covers fundamental concepts in recursion, computational complexity, and intractable problems. We will explore classic problems, their computational challenges, and the classes P, NP, and NP-completeness, with clear explanations and examples.

---

## 1. Recursive Programming

### What is Recursion?
Recursion is when a function calls itself to solve a smaller version of the same problem. It usually has:
- **Base case:** The simplest instance, which can be solved directly (no more recursion).
- **Recursive case:** The function calls itself with a smaller/simpler input.

#### Example: Factorial Function
```c
int factorial(int n) { // assume n >= 0
  if (n == 0)
    return 1;
  else
    return n * factorial(n-1);
}
```

How it works:
- When you call `factorial(3)`, it keeps calling itself until it reaches the base case:
  - `factorial(3)` calls `factorial(2)`
  - `factorial(2)` calls `factorial(1)`
  - `factorial(1)` calls `factorial(0)`
  - `factorial(0)` returns 1
- Then, the results are multiplied as the calls return:
  - `factorial(1)` returns `1 * 1 = 1`
  - `factorial(2)` returns `2 * 1 = 2`
  - `factorial(3)` returns `3 * 2 = 6`

**Key idea:** Recursion breaks a problem into smaller pieces, solves the smallest piece first, and combines results as the calls return.

---

## 2. Towers of Hanoi

### Problem Statement
- **Goal:** Transfer all $n$ disks from peg A to peg B.
- **Rules:**
  - Move one disk at a time.
  - Never place a larger disk above a smaller one.

### Recursive Solution
- Brute force is hard for large $n$.
- Recursive approach:
    1. Move the top $n-1$ disks from A to C using B as auxiliary.
    2. Move the remaining disk from A to B.
    3. Move the $n-1$ disks from C to B using A as auxiliary.

#### Example Code (C):
```c
void hanoi(int n, char a, char b, char c) {
    if (n > 0) {
        hanoi(n-1, a, c, b);
        printf("Move disk of diameter %d from %c to %c\n", n, a, b);
        hanoi(n-1, c, b, a);
    }
}
// Example call: hanoi(5, 'A', 'B', 'C');
```

### Recurrence Relation
- $T(n) = 2T(n-1) + 1$
- $T(1) = 1$

#### Solution by Unfolding
Expand the recurrence:
$$
T(n) = 2T(n-1) + 1 \\
= 2(2T(n-2) + 1) + 1 \\
= 4T(n-2) + 2 + 1 \\
= 8T(n-3) + 4 + 2 + 1 \\
= \ldots \\
= 2^i T(n-i) + 2^{i-1} + 2^{i-2} + \ldots + 2^1 + 2^0
$$
The expansion stops when $i = n-1$:
$$
T(n) = 2^{n-1} + 2^{n-2} + \ldots + 2^0
$$
This is a geometric series:
$$
T(n) = 2^n - 1
$$

**Key Takeaway:**
- The minimum number of moves required is $2^n - 1$ (exponential growth).

---

## 3. Complexity and Growth Rates

### What is Complexity?
Complexity measures how the resources (time, space) needed by an algorithm grow as the input size increases.

- **Polynomial functions** (like $n$, $n^2$, $n^3$) are considered **good**. Algorithms with polynomial time complexity are usually practical and efficient for large inputs.
- **Super-polynomial** (especially **exponential**) functions (like $2^n$, $n!$) are considered **bad**. Algorithms with these complexities become intractable (impractical) very quickly as input size grows.

**Key idea:**
- If an algorithm runs in polynomial time, it is generally considered efficient.
- If it runs in super-polynomial or exponential time, it is considered intractable for large inputs.

---

## 4. Tractable vs. Intractable Problems & Growth Rates

### Reasonable vs. Unreasonable Growth
- **Tractable:** Problems with polynomial-time algorithms ($n^k$).
- **Intractable:** Problems with super-polynomial time (above $n^k$).

| Function | $n=10$ | $n=20$ | $n=50$ | $n=100$ | $n=300$ |
|----------|--------|--------|--------|---------|---------|
| $n^2$    | microseconds | microseconds | microseconds | microseconds | microseconds |
| $n^5$    | 0.1s   | 3.2s   | 5.2min | 2.8hr   | 28.1d   |
| $2^n$    | 0.001s | 1s     | 35.7yr | 400T centuries | huge |
| $n^n$    | 2.8hr  | 3.3Tyr | huge   | huge    | huge    |

**Key point:** Exponential and super-exponential growth quickly outpace any hardware improvements.

---

## 5. Monkey Puzzle: Complexity Example

### Problem Description
- You have 25 square cards, each with "monkey halves" imprinted.
- The goal: Arrange the cards in a 5x5 square so that matching halves and colors are identical wherever edges meet.

### Brute Force Solution
- Try every possible arrangement of the cards.
- For 25 cards:
    - 25 choices for the first card
    - 24 for the second
    - 23 for the third, and so on...
- Total arrangements: $25 \times 24 \times 23 \times \ldots \times 1 = 25!$
- $25!$ is a number with 26 digits!
- If a computer checks 1,000,000 arrangements per second, it would still take about 490 billion years to check all possibilities.

### Why is it so hard?
- The number of possible arrangements grows extremely fast (factorial growth).
- Even with fast computers, brute force is not practical for large $n$.

### Smarter Algorithms
- Techniques like backtracking and pruning can discard impossible partial arrangements early.
- However, even the smartest known algorithms can take thousands of years in the worst case for $n=25$.
- No one has found a truly efficient (polynomial-time) solution for this type of problem yet.

**Key Takeaway:**
Some problems are so complex that even the best computers and algorithms can't solve them quickly as the problem size grows. This is a key idea in computational complexity theory.

---

## 6. Travelling Salesman Problem (TSP) & Hamiltonian Cycle

### Travelling Salesman Problem (TSP)
- **Definition:** Given a set of cities and distances between them, find the shortest possible route that visits each city exactly once and returns to the starting city.
- **Complexity:** Naive solutions take $n!$ time (factorial), where $n$ is the number of cities. No polynomial-time algorithm is known. TSP is an NP-complete problem.

### Hamiltonian Cycle Problem (HCP)
- **Definition:** Given a graph $G = (V, E)$, a Hamiltonian cycle is an ordering of the vertices such that each vertex is visited exactly once and the cycle returns to the starting vertex.
- TSP is a weighted version of HCP. Both are NP-complete.

### Variants of TSP
- TSP and its variants appear in many real-world applications:
    - Design of telephone networks and integrated circuits
    - Planning construction lines
    - Programming industrial robots

---

## 7. Coloring Problem

### 3-Coloring
- Given a planar map, can it be colored using 3 colors so that no adjacent regions have the same color?
- Some maps can be 3-colored (YES instance), others cannot (NO instance, e.g., Nevada and bordering states).

### 4-Color Theorem
- Any map can be colored with 4 colors.

### 2-Coloring
- Maps with no points that are the junctions of an odd number of states can be 2-colored.

### Complexity
- No polynomial-time algorithms are known for 3-coloring; it is NP-complete.

---

## 8. Satisfiability (SAT)

### What is SAT?
- **Definition:** Determine the truth or falsity of formulae in Boolean algebra (propositional calculus).
- Boolean variables and operators: $\land$ (and), $\lor$ (or), $\lnot$ (not).
- Example: $\varphi = (\lnot x \land y) \lor (x \land \lnot z)$

### The SAT Problem
- Is there an assignment of values to variables that makes the formula TRUE?
- Example: $x=0, y=1, z=0$ makes $\varphi$ true.

### Complexity
- Exponential time algorithm on $n$ variables: $O(2^n)$
- Best known solution: SAT is NP-complete.

---

## 9. Clique Problem

### What is a Clique?
- **Definition:** Given $n$ people and their pairwise relationships (friendships), is there a group of $s$ people such that every pair in the group knows each other?
- In graph terms: Given a graph, does it contain a complete subgraph (clique) of size $s$?

### Example
- People: $a, b, c, ..., k$
- Friendships: $(a, e), (a, f), ...$
- Clique size: $s = 4$?
- YES, the set $\{b, d, i, h\}$ forms a clique of size 4 (every pair among them are friends).
- This set is called a **certificate** (a proof that a clique of size $s$ exists).

### Complexity
- The clique problem is NP-complete: no polynomial-time algorithm is known for finding the largest clique in a general graph.

---

## 10. P: Polynomial-Time Problems

### What is P?
- **Definition:** P is the set of all decision problems solvable in polynomial time on a deterministic Turing machine (i.e., a real computer).

### Examples
- MULTIPLE: Is the integer $y$ a multiple of $x$? (e.g., $x=17$, $y=51$ → YES)
- RELPRIME (co-prime): Are $x$ and $y$ relatively prime? (e.g., $x=34$, $y=39$ → YES)

---

## 11. Determinism & Non-determinism

### Deterministic Computation
- When a machine is in a given state and reads the next input symbol, the next state is uniquely determined.

### Non-deterministic Computation
- Several choices may exist for the next state.

---

## 12. Turing Machines

- Proposed by Alan Turing in 1936.
- Can do anything a general-purpose computer can do.
- But there exist problems that even Turing machines (and thus computers) cannot solve—these are beyond the limits of theoretical computation.

---

## 13. NP: Nondeterministic Polynomial Time

### What is NP?
- **Definition:** NP is the set of all decision problems solvable in polynomial time on a nondeterministic Turing machine.
- No known polynomial-time solutions to NP problems.

### Alternative Definition
- Set of all decision problems with efficient (polynomial-time) verification algorithms on a deterministic Turing machine.

### Key Point
- NP = problems with efficient verification, but not necessarily efficient solution algorithms.
- To solve, you would need to "guess" a certificate and verify it; naive simulation takes exponential time unless you get lucky.

---

## 14. NP-Completeness

### What is NP-hard?
- A problem at least as hard as any problem in NP (any NP problem can be reduced to it in polynomial time).

### What is NP-complete?
- Problems in NP that are also NP-hard (the "hardest" problems in NP).

### Formal Definition
- A problem $B$ is NP-complete if:
    - $B$ is in NP
    - Every problem $A$ in NP is polynomial-time reducible to $B$

### Key Points
- All NP-complete problems are tightly coupled: finding a polynomial-time algorithm for one would solve all NP problems efficiently.
- Proving one NP-complete problem requires exponential time would prove all do.

- The order of complexity for some algorithms, like the Travelling Salesman Problem (TSP), is $O(n!)$ (factorial time).
  - $n!$ grows much faster than polynomial functions ($n^2$, $n^3$, etc.).
  - For example, $25!$ is a 26-digit number—impossible to compute exhaustively even with fast computers.
- Some functions grow even faster, like $n^n$ (super-exponential).
- Even $2^n$ (exponential) becomes unmanageable for modest $n$.

### Reasonable vs. Unreasonable Growth Rates
- **Reasonable (tractable):**
  - Algorithms with polynomial time complexity ($n^k$) are considered efficient and practical.
- **Unreasonable (intractable):**
  - Algorithms with super-polynomial or exponential time ($2^n$, $n!$, $n^n$) are impractical for large $n$.
- Example table (approximate times for $n$):

| Function | $n=10$ | $n=20$ | $n=50$ | $n=100$ | $n=300$ |
|----------|--------|--------|--------|---------|---------|
| $n^2$    | microseconds | microseconds | microseconds | microseconds | microseconds |
| $n^5$    | 0.1s   | 3.2s   | 5.2min | 2.8hr   | 28.1d   |
| $2^n$    | 0.001s | 1s     | 35.7yr | 400T centuries | huge |
| $n^n$    | 2.8hr  | 3.3Tyr | huge   | huge    | huge    |

**Key point:** Exponential and super-exponential growth quickly outpace any hardware improvements.

### Tractable vs. Intractable Problems
- **Tractable:** Problems with polynomial-time algorithms ($n^k$).
- **Intractable:** Problems with super-polynomial time (above $n^k$).
- Some problems (like the Monkey Puzzle) are known as NP-complete (NPC):
  - Many such problems exist (~1000 known)
  - All known solutions are unreasonable (super-polynomial)
  - No polynomial-time solutions are known

## Travelling Salesman Problem (TSP)

- **Definition:**
  - Given a set of cities and distances between them, find the shortest possible route that visits each city exactly once and returns to the starting city.
- **Complexity:**
  - Naive solutions take $n!$ time (factorial), where $n$ is the number of cities.
  - No polynomial-time algorithm is known.
  - TSP is an NP-complete problem.
- **Related:**
  - The Longest Path problem in a weighted graph is also NP-complete.
## Complexity and Intractability

- In computer science, we classify the growth of functions (which describe algorithm running times) as 'good' or 'bad':
  - **Polynomial functions** (like $n$, $n^2$, $n^3$) are considered **good**. Algorithms with polynomial time complexity are usually practical and efficient for large inputs.
  - **Super-polynomial** (especially **exponential**) functions (like $2^n$, $n!$) are considered **bad**. Algorithms with these complexities become intractable (impractical) very quickly as input size grows.

- **Key idea:**
  - If an algorithm runs in polynomial time, it is generally considered efficient.
  - If it runs in super-polynomial or exponential time, it is considered intractable for large inputs.
## Monkey Puzzle: Complexity Example

### Problem Description
- You have 25 square cards, each with "monkey halves" imprinted.
- The goal: Arrange the cards in a 5x5 square so that matching halves and colors are identical wherever edges meet.

### Brute Force Solution
- Try every possible arrangement of the cards.
- For 25 cards:
  - 25 choices for the first card
  - 24 for the second
  - 23 for the third, and so on...
- Total arrangements: $25 \times 24 \times 23 \times \ldots \times 1 = 25!$
- $25!$ is a number with 26 digits!
- If a computer checks 1,000,000 arrangements per second, it would still take about 490 billion years to check all possibilities.

### Why is it so hard?
- The number of possible arrangements grows extremely fast (factorial growth).


# Lecture 4: Recursion, Complexity, and Intractable Problems

## 1. Recursive Programming

### What is Recursion?
Recursion is when a function calls itself to solve a smaller version of the same problem. It usually has:
- **Base case:** The simplest instance, which can be solved directly (no more recursion).
- **Recursive case:** The function calls itself with a smaller/simpler input.

#### Example: Factorial Function
```c
int factorial(int n) { // assume n >= 0
  if (n == 0)
  return 1;
  else
  return n * factorial(n-1);
}
```

How it works:
- When you call `factorial(3)`, it keeps calling itself until it reaches the base case:
  - `factorial(3)` calls `factorial(2)`
  - `factorial(2)` calls `factorial(1)`
  - `factorial(1)` calls `factorial(0)`
  - `factorial(0)` returns 1
- Then, the results are multiplied as the calls return:
  - `factorial(1)` returns `1 * 1 = 1`
  - `factorial(2)` returns `2 * 1 = 2`
  - `factorial(3)` returns `3 * 2 = 6`

Key idea: Recursion breaks a problem into smaller pieces, solves the smallest piece first, and combines results as the calls return.

## 2. Towers of Hanoi

### Problem Statement
- **Goal:** Transfer all $n$ disks from peg A to peg B.
- **Rules:**
  - Move one disk at a time.
  - Never place a larger disk above a smaller one.

### Recursive Solution
- Brute force is hard for large $n$.
- Recursive approach:
  1. Move the top $n-1$ disks from A to C using B as auxiliary.
  2. Move the remaining disk from A to B.
  3. Move the $n-1$ disks from C to B using A as auxiliary.

#### Example Code (C):
```c
void hanoi(int n, char a, char b, char c) {
  if (n > 0) {
    hanoi(n-1, a, c, b);
    printf("Move disk of diameter %d from %c to %c\n", n, a, b);
    hanoi(n-1, c, b, a);
  }
}
// Example call: hanoi(5, 'A', 'B', 'C');
```

### Recurrence Relation
- $T(n) = 2T(n-1) + 1$
- $T(1) = 1$

#### Solution by Unfolding
Expand the recurrence:
$$
T(n) = 2T(n-1) + 1 \\
= 2(2T(n-2) + 1) + 1 \\
= 4T(n-2) + 2 + 1 \\
= 8T(n-3) + 4 + 2 + 1 \\
= \ldots \\
= 2^i T(n-i) + 2^{i-1} + 2^{i-2} + \ldots + 2^1 + 2^0
$$
The expansion stops when $i = n-1$:
$$
T(n) = 2^{n-1} + 2^{n-2} + \ldots + 2^0
$$
This is a geometric series:
$$
T(n) = 2^n - 1
$$

**Key Takeaway:**
- The minimum number of moves required is $2^n - 1$ (exponential growth).

## 3. Complexity and Growth Rates

- In computer science, we classify the growth of functions (which describe algorithm running times) as 'good' or 'bad':
  - **Polynomial functions** (like $n$, $n^2$, $n^3$) are considered **good**. Algorithms with polynomial time complexity are usually practical and efficient for large inputs.
  - **Super-polynomial** (especially **exponential**) functions (like $2^n$, $n!$) are considered **bad**. Algorithms with these complexities become intractable (impractical) very quickly as input size grows.

- **Key idea:**
  - If an algorithm runs in polynomial time, it is generally considered efficient.
  - If it runs in super-polynomial or exponential time, it is considered intractable for large inputs.

## 4. Tractable vs. Intractable Problems & Growth Rates

- **Reasonable (tractable):**
  - Algorithms with polynomial time complexity ($n^k$) are considered efficient and practical.
- **Unreasonable (intractable):**
  - Algorithms with super-polynomial or exponential time ($2^n$, $n!$, $n^n$) are impractical for large $n$.
- Example table (approximate times for $n$):

| Function | $n=10$ | $n=20$ | $n=50$ | $n=100$ | $n=300$ |
|----------|--------|--------|--------|---------|---------|
| $n^2$    | microseconds | microseconds | microseconds | microseconds | microseconds |
| $n^5$    | 0.1s   | 3.2s   | 5.2min | 2.8hr   | 28.1d   |
| $2^n$    | 0.001s | 1s     | 35.7yr | 400T centuries | huge |
| $n^n$    | 2.8hr  | 3.3Tyr | huge   | huge    | huge    |

**Key point:** Exponential and super-exponential growth quickly outpace any hardware improvements.

## 5. Monkey Puzzle: Complexity Example

### Problem Description
- You have 25 square cards, each with "monkey halves" imprinted.
- The goal: Arrange the cards in a 5x5 square so that matching halves and colors are identical wherever edges meet.

### Brute Force Solution
- Try every possible arrangement of the cards.
- For 25 cards:
  - 25 choices for the first card
  - 24 for the second
  - 23 for the third, and so on...
- Total arrangements: $25 \times 24 \times 23 \times \ldots \times 1 = 25!$
- $25!$ is a number with 26 digits!
- If a computer checks 1,000,000 arrangements per second, it would still take about 490 billion years to check all possibilities.

### Why is it so hard?
- The number of possible arrangements grows extremely fast (factorial growth).
- Even with fast computers, brute force is not practical for large $n$.

### Smarter Algorithms
- Techniques like backtracking and pruning can discard impossible partial arrangements early.
- However, even the smartest known algorithms can take thousands of years in the worst case for $n=25$.
- No one has found a truly efficient (polynomial-time) solution for this type of problem yet.

### Key Takeaway
Some problems are so complex that even the best computers and algorithms can't solve them quickly as the problem size grows. This is a key idea in computational complexity theory.

## 6. Travelling Salesman Problem (TSP) & Hamiltonian Cycle

- **Travelling Salesman Problem (TSP):**
  - Given a set of cities and distances between them, find the shortest possible route that visits each city exactly once and returns to the starting city.
  - Naive solutions take $n!$ time (factorial), where $n$ is the number of cities.
  - No polynomial-time algorithm is known.
  - TSP is an NP-complete problem.
- **Hamiltonian Cycle Problem (HCP):**
  - Given a graph $G = (V, E)$, a Hamiltonian cycle is an ordering of the vertices such that each vertex is visited exactly once and the cycle returns to the starting vertex.
  - TSP is a weighted version of HCP. Both are NP-complete.

### 7. Variants of TSP
- TSP and its variants appear in many real-world applications:
  - Design of telephone networks and integrated circuits
  - Planning construction lines
  - Programming industrial robots

## 8. Coloring Problem

- **3-Coloring:**
  - Given a planar map, can it be colored using 3 colors so that no adjacent regions have the same color?
  - Some maps can be 3-colored (YES instance), others cannot (NO instance, e.g., Nevada and bordering states).
- **4-Color Theorem:**
  - Any map can be colored with 4 colors.
- **2-Coloring:**
  - Maps with no points that are the junctions of an odd number of states can be 2-colored.
- **Complexity:**
  - No polynomial-time algorithms are known for 3-coloring; it is NP-complete.

## 9. Satisfiability (SAT)

- **Definition:**
  - Determine the truth or falsity of formulae in Boolean algebra (propositional calculus).
  - Boolean variables and operators: $\land$ (and), $\lor$ (or), $\lnot$ (not).
  - Example: $\varphi = (\lnot x \land y) \lor (x \land \lnot z)$
- **The SAT Problem:**
  - Is there an assignment of values to variables that makes the formula TRUE?
  - Example: $x=0, y=1, z=0$ makes $\varphi$ true.
- **Complexity:**
  - Exponential time algorithm on $n$ variables: $O(2^n)$
  - Best known solution: SAT is NP-complete.

## 10. Clique Problem

- **Definition:**
  - Given $n$ people and their pairwise relationships (friendships), is there a group of $s$ people such that every pair in the group knows each other?
  - In graph terms: Given a graph, does it contain a complete subgraph (clique) of size $s$?

- **Example:**
  - People: $a, b, c, ..., k$
  - Friendships: $(a, e), (a, f), ...$
  - Clique size: $s = 4$?
  - YES, the set $\{b, d, i, h\}$ forms a clique of size 4 (every pair among them are friends).
  - This set is called a **certificate** (a proof that a clique of size $s$ exists).

- **Complexity:**
  - The clique problem is NP-complete: no polynomial-time algorithm is known for finding the largest clique in a general graph.

## 11. P: Polynomial-Time Problems

- **Definition:**
  - P is the set of all decision problems solvable in polynomial time on a deterministic Turing machine (i.e., a real computer).
- **Examples:**
  - MULTIPLE: Is the integer $y$ a multiple of $x$? (e.g., $x=17$, $y=51$ → YES)
  - RELPRIME (co-prime): Are $x$ and $y$ relatively prime? (e.g., $x=34$, $y=39$ → YES)

## 12. Determinism & Non-determinism

- **Deterministic computation:**
  - When a machine is in a given state and reads the next input symbol, the next state is uniquely determined.
- **Non-deterministic computation:**
  - Several choices may exist for the next state.

## 13. Turing Machines

- Proposed by Alan Turing in 1936.
- Can do anything a general-purpose computer can do.
- But there exist problems that even Turing machines (and thus computers) cannot solve—these are beyond the limits of theoretical computation.

## 14. NP: Nondeterministic Polynomial Time

- **Definition:**
  - NP is the set of all decision problems solvable in polynomial time on a nondeterministic Turing machine.
  - No known polynomial-time solutions to NP problems.
- **Alternative definition:**
  - Set of all decision problems with efficient (polynomial-time) verification algorithms on a deterministic Turing machine.
- **Key point:**
  - NP = problems with efficient verification, but not necessarily efficient solution algorithms.
  - To solve, you would need to "guess" a certificate and verify it; naive simulation takes exponential time unless you get lucky.

## 15. NP-Completeness

- **NP-hard:**
  - A problem at least as hard as any problem in NP (any NP problem can be reduced to it in polynomial time).
- **NP-complete:**
  - Problems in NP that are also NP-hard (the "hardest" problems in NP).
- **Formal definition:**
  - A problem $B$ is NP-complete if:
    - $B$ is in NP
    - Every problem $A$ in NP is polynomial-time reducible to $B$
- **Key points:**
  - All NP-complete problems are tightly coupled: finding a polynomial-time algorithm for one would solve all NP problems efficiently.
  - Proving one NP-complete problem requires exponential time would prove all do.

## 1. Recursive Programming

### What is Recursion?
Recursion is when a function calls itself to solve a smaller version of the same problem. It usually has:
- **Base case:** The simplest instance, which can be solved directly (no more recursion).
- **Recursive case:** The function calls itself with a smaller/simpler input.

#### Example: Factorial Function
```c
int factorial(int n) { // assume n >= 0
  if (n == 0)
    return 1;
  else
    return n * factorial(n-1);
}
```

How it works:
- When you call `factorial(3)`, it keeps calling itself until it reaches the base case:
  - `factorial(3)` calls `factorial(2)`
  - `factorial(2)` calls `factorial(1)`
  - `factorial(1)` calls `factorial(0)`
  - `factorial(0)` returns 1
- Then, the results are multiplied as the calls return:
  - `factorial(1)` returns `1 * 1 = 1`
  - `factorial(2)` returns `2 * 1 = 2`
  - `factorial(3)` returns `3 * 2 = 6`

Key idea: Recursion breaks a problem into smaller pieces, solves the smallest piece first, and combines results as the calls return.

## 2. Towers of Hanoi

### Problem Statement
- **Goal:** Transfer all $n$ disks from peg A to peg B.
- **Rules:**
  - Move one disk at a time.
  - Never place a larger disk above a smaller one.

### Recursive Solution
- Brute force is hard for large $n$.
- Recursive approach:
    1. Move the top $n-1$ disks from A to C using B as auxiliary.
    2. Move the remaining disk from A to B.
    3. Move the $n-1$ disks from C to B using A as auxiliary.

#### Example Code (C):
```c
void hanoi(int n, char a, char b, char c) {
    if (n > 0) {
        hanoi(n-1, a, c, b);
        printf("Move disk of diameter %d from %c to %c\n", n, a, b);
        hanoi(n-1, c, b, a);
    }
}
// Example call: hanoi(5, 'A', 'B', 'C');
```

### Recurrence Relation
- $T(n) = 2T(n-1) + 1$
- $T(1) = 1$

#### Solution by Unfolding
Expand the recurrence:
$$
T(n) = 2T(n-1) + 1 \\
= 2(2T(n-2) + 1) + 1 \\
= 4T(n-2) + 2 + 1 \\
= 8T(n-3) + 4 + 2 + 1 \\
= \ldots \\
= 2^i T(n-i) + 2^{i-1} + 2^{i-2} + \ldots + 2^1 + 2^0
$$
The expansion stops when $i = n-1$:
$$
T(n) = 2^{n-1} + 2^{n-2} + \ldots + 2^0
$$
This is a geometric series:
$$
T(n) = 2^n - 1
$$

**Key Takeaway:**
- The minimum number of moves required is $2^n - 1$ (exponential growth).

## 3. Monkey Puzzle: Complexity Example

### Problem Description
- You have 25 square cards, each with "monkey halves" imprinted.
- The goal: Arrange the cards in a 5x5 square so that matching halves and colors are identical wherever edges meet.

### Brute Force Solution
- Try every possible arrangement of the cards.
- For 25 cards:
    - 25 choices for the first card
    - 24 for the second
    - 23 for the third, and so on...
- Total arrangements: $25 \times 24 \times 23 \times \ldots \times 1 = 25!$
- $25!$ is a number with 26 digits!
- If a computer checks 1,000,000 arrangements per second, it would still take about 490 billion years to check all possibilities.

### Why is it so hard?
- The number of possible arrangements grows extremely fast (factorial growth).
- Even with fast computers, brute force is not practical for large $n$.

### Smarter Algorithms
- Techniques like backtracking and pruning can discard impossible partial arrangements early.
- However, even the smartest known algorithms can take thousands of years in the worst case for $n=25$.
- No one has found a truly efficient (polynomial-time) solution for this type of problem yet.

### Key Takeaway
Some problems are so complex that even the best computers and algorithms can't solve them quickly as the problem size grows. This is a key idea in computational complexity theory.

## 4. Complexity and Intractability

- In computer science, we classify the growth of functions (which describe algorithm running times) as 'good' or 'bad':
    - **Polynomial functions** (like $n$, $n^2$, $n^3$) are considered **good**. Algorithms with polynomial time complexity are usually practical and efficient for large inputs.
    - **Super-polynomial** (especially **exponential**) functions (like $2^n$, $n!$) are considered **bad**. Algorithms with these complexities become intractable (impractical) very quickly as input size grows.

- **Key idea:**
    - If an algorithm runs in polynomial time, it is generally considered efficient.
    - If it runs in super-polynomial or exponential time, it is considered intractable for large inputs.

## 5. Complexity and Intractability (continued)

- The order of complexity for some algorithms, like the Travelling Salesman Problem (TSP), is $O(n!)$ (factorial time).
    - $n!$ grows much faster than polynomial functions ($n^2$, $n^3$, etc.).
    - For example, $25!$ is a 26-digit number—impossible to compute exhaustively even with fast computers.
- Some functions grow even faster, like $n^n$ (super-exponential).
- Even $2^n$ (exponential) becomes unmanageable for modest $n$.

### Reasonable vs. Unreasonable Growth Rates
- **Reasonable (tractable):**
    - Algorithms with polynomial time complexity ($n^k$) are considered efficient and practical.
- **Unreasonable (intractable):**
    - Algorithms with super-polynomial or exponential time ($2^n$, $n!$, $n^n$) are impractical for large $n$.
- Example table (approximate times for $n$):

| Function | $n=10$ | $n=20$ | $n=50$ | $n=100$ | $n=300$ |
|----------|--------|--------|--------|---------|---------|
| $n^2$    | microseconds | microseconds | microseconds | microseconds | microseconds |
| $n^5$    | 0.1s   | 3.2s   | 5.2min | 2.8hr   | 28.1d   |
| $2^n$    | 0.001s | 1s     | 35.7yr | 400T centuries | huge |
| $n^n$    | 2.8hr  | 3.3Tyr | huge   | huge    | huge    |

**Key point:** Exponential and super-exponential growth quickly outpace any hardware improvements.

### Tractable vs. Intractable Problems
- **Tractable:** Problems with polynomial-time algorithms ($n^k$).
- **Intractable:** Problems with super-polynomial time (above $n^k$).
- Some problems (like the Monkey Puzzle) are known as NP-complete (NPC):
    - Many such problems exist (~1000 known)
    - All known solutions are unreasonable (super-polynomial)
    - No polynomial-time solutions are known

## 6. Travelling Salesman Problem (TSP)

- **Definition:**
    - Given a set of cities and distances between them, find the shortest possible route that visits each city exactly once and returns to the starting city.
- **Complexity:**
    - Naive solutions take $n!$ time (factorial), where $n$ is the number of cities.
    - No polynomial-time algorithm is known.
    - TSP is an NP-complete problem.
- **Related:**
    - The Longest Path problem in a weighted graph is also NP-complete.
