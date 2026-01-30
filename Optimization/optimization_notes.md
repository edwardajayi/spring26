# Reading Notes - Optimization

## Weekly Readings

## Questions

### Condition for Optimal Vector $x^*$

**Standard Form:**
$$
\begin{array}{ll}
\text{minimize} & f_0(x) \\
\text{subject to} & f_i(x) \le b_i, \quad i=1, \dots, m.
\end{array}
$$


**Definition:**
A vector $x^*$ is optimal if:
1.  It is **feasible**: It satisfies all constraints $f_i(x^*) \le b_i$ for $i=1, \dots, m$.
2.  It is **minimal**: For any other feasible vector $z$ (i.e., any $z$ satisfying the constraints), the objective function value at $z$ is greater than or equal to the value at $x^*$: $f_0(z) \ge f_0(x^*)$.

**Explanation:**
Think of the problem as finding the "best" point within a allowed region.
- The **constraints** define the allowed region (the feasible set). If a point $z$ doesn't satisfy these, it's not even a candidate (it's infeasible).
- The **objective function** $f_0$ measures the "cost" of each point. We want to minimize this cost.
- The condition $f_0(z) \ge f_0(x^*)$ simply means that no matter which other valid candidate $z$ you pick, you cannot find one with a lower cost than $x^*$. Thus, $x^*$ is the global minimum within the feasible region.

### Linear vs. Convex Optimization

Convex optimization can be seen as a **generalization** of linear programming.

*   **Linear Program**: A specific family of optimization problems where objective and constraint functions are *linear*. They satisfy:
    $$f_i(\alpha x + \beta y) = \alpha f_i(x) + \beta f_i(y)$$
    for all $x, y \in \mathbf{R}^n$ and all $\alpha, \beta \in \mathbf{R}$.

*   **Convex Optimization Problem**: A broader class where functions are *convex*. They satisfy the inequality:
    $$f_i(\alpha x + \beta y) \le \alpha f_i(x) + \beta f_i(y)$$
    for all $x, y \in \mathbf{R}^n$ and all $\alpha, \beta \in \mathbf{R}$ with $\alpha + \beta = 1, \alpha \ge 0, \beta \ge 0$.

### Objective Function vs. Objective Value

It's important to distinguish between the function itself and the value it produces:

*   **Objective Function ($f_0$):**
    *   This is the **rule** or **formula** (the map).
    *   It takes a vector $x$ as input and returns a real number.
    *   *Example:* $f_0(x) = x^2 + 2x$.

*   **Objective Value ($f_0(x)$):**
    *   This is the **number** you get when you plug a specific point $x$ into the function.
    *   *Example:* If $x=3$, the objective value is $f_0(3) = 3^2 + 2(3) = 15$.
### Least-Squares Problems

A basic type of optimization problem with **no constraints**.

**Definition:**
$$
\text{minimize} \quad \|Ax - b\|_2^2 = \sum_{i=1}^k (a_i^T x - b_i)^2
$$

**What does $m=0$ mean?**
*   In the standard form, $m$ is the number of inequality constraints ($f_i(x) \le b_i$).
*   **$m=0$ simple means there are ZERO constraints.**
*   You are free to choose *any* vector $x$ (it's an "unconstrained" problem). The entire vector space is feasible.

**Simplified Explanation:**
You have a set of linear equations $Ax = b$ that might not have a perfect solution (because you have more equations than variables, "overdetermined").
Since you can't make the error zero (can't solve perfectly), you try to find the $x$ that makes the **error as small as possible**.
*   We minimize the "sum of squares" of the errors (the distance between $Ax$ and $b$).
### Least-Squares Extensions

Standard techniques to increase flexibility.

#### 1. Weighted Least-Squares
**Definition:**
$$
\text{minimize} \quad \sum_{i=1}^k w_i (a_i^T x - b_i)^2
$$
where weights $w_1, \dots, w_k$ are positive.

**The "Minimizing Cost" Idea:**
Imagine each term $(a_i^T x - b_i)^2$ is a "cost" or "penalty" for being wrong on measurement $i$.
*   **Standard LS:** All errors cost the same. Being off by 1 unit on measurement #1 costs you \$1. Being off by 1 unit on measurement #2 costs you \$1.
*   **Weighted LS:** Errors cost different amounts.
    *   If $w_1 = 100$ and $w_2 = 1$, then being off by 1 unit on measurement #1 costs you **\$100**, while measurement #2 only costs **\$1**.
    *   **Result:** The optimizer will work *much harder* to make measurement #1 accurate, even if it means sacrificing accuracy on measurement #2.
*   **Use Case:** Sensor fusion. You have a \$10,000 high-precision GPS (high weight) and a \$5 phone GPS (low weight). You trust the expensive one more.

#### 2. Regularization
**Definition:**
$$
\sum_{i=1}^k (a_i^T x - b_i)^2 + \rho \sum_{j=1}^n x_j^2
$$
where $\rho > 0$ is a user-chosen parameter.
*   **Purpose:** Adds a **penalty** for large values of $x$. The extra term $\rho \sum x_j^2$ makes the cost go up if elements of $x$ get too big.
*   **Trade-off:** The parameter $\rho$ controls the balance between fitting the data well (minimizing the first part) and keeping $x$ small (minimizing the second part).

### How to Recognize a Least-Squares Problem

You can identify a problem as a candidate for Least Squares if it meets two criteria:

1.  **The Objective is a Quadratic Function:**
    It looks like "sum of squares".
    *   Look for terms like $(expression)^2$ or vectors norms $\| \dots \|_2^2$.
    *   Mathematically, is it in the form $x^T P x + q^T x + r$ (where $P$ is positive semidefinite)?

2.  **No Inequality Constraints:**
    *   Are there rules like "$x$ must be less than 5"? If **YES**, it's **NOT** a standard Least Squares problem (it might be Quadratic Programming).
    *   Equality constraints ($Ax=b$) are okay (can be eliminated), but simple LS usually implies unconstrained ($m=0$).

### Connection: Least Squares $\to$ Quadratic Form (What is P?)
You might look at the form $x^T P x$ and ask: **"Do we solve for $P$?"**

**NO.**
*   **$x$ is the Variable:** This is what we don't know and want to find.
*   **$P$ is Data (Constant):** This is given to us or calculated from our inputs.

For Least Squares, we usually start with data matrix $A$. We can **derive** $P$ from $A$ by expanding the squares:
$$
\begin{aligned}
\|Ax - b\|_2^2 &= (Ax - b)^T (Ax - b) \\
&= \underbrace{x^T A^T A x}_{\text{Quadratic Part}} - \underbrace{2b^T A x}_{\text{Linear Part}} + \underbrace{b^T b}_{\text{Constant}}
\end{aligned}
$$
Matching this to the general quadratic form $x^T P x + q^T x + r$:
*   **$P = A^T A$** (We calculate this from our known data $A$)
*   $q = -2A^T b$
*   $r = b^T b$

**Conclusion:** We don't solve for $P$. We compute $P$ from our data, then use it to solve for $x$.


### Concrete Examples

**Example 1: Linear Regression (Data Fitting)**
*   **Goal:** Fit a line $y = \alpha t + \beta$ through scattered points.
*   **Unknowns ($x$):** The slope $\alpha$ and intercept $\beta$.
*   **The Cost:** $\sum (\text{actual } y - \text{predicted } y)^2$.
*   **Why LS?** We want to minimize the total squared distance from the dots to the line.

**Example 2: Signal Recovery**
*   **Goal:** You receive a noisy signal $y = Ax + \text{noise}$. You want to find the original signal $x$.
*   **The Cost:** $\|Ax - y\|^2$.
*   **Why LS?** Finding the $x$ that "best explains" the received signal $y$ under the assumption of Gaussian noise.
### Is "Solving" Least-Squares a Problem?

**Short Answer: No.**
In the world of optimization, Least-Squares is considered a **solved problem**.
*   We have efficient algorithms (using matrix operations like QR factorization or SVD) that can solve these very fast.
*   "Solving" it is about as standard and reliable as solving a simple equation like $2x = 4$.

**Machine Learning Context:**
You often see this in ML as **Linear Regression**.
*   **The Problem:** minimizing the error between your model's predictions ($Ax$) and the actual data labels ($b$).
*   **The "Problem" in ML:** While the *math* is solved, the *size* can be an issue.
    *   If you have **billions** of data points (rows in $A$), you can't just plug it into the formula $(A^T A)^{-1} A^T b$ because the matrix $A^T A$ is too huge to invert in memory.
    *   **Solution:** That's why in Deep Learning/Big Data, we use **iterative methods** (like Gradient Descent) to step towards the answer, rather than calculating it in one giant shot. But analytically, it is well-understood.






