# Problem 1: Convex Functions Solutions

## (a) $f(x) = \frac{1}{x^2}$ over domain $(0, \infty)$

**Answer: Strictly Convex**

To determine the convexity, we examine the second derivative of the function $f(x) = x^{-2}$.

First derivative:
$$ f'(x) = -2x^{-3} $$

Second derivative:
$$ f''(x) = 6x^{-4} = \frac{6}{x^4} $$

Since the domain is $(0, \infty)$, $x > 0$, which implies $x^4 > 0$.
Therefore, $f''(x) = \frac{6}{x^4} > 0$ for all $x \in (0, \infty)$.

Since the second derivative is strictly positive everywhere on the domain, the function is **strictly convex**.

It is not $\mu$-strongly convex because as $x \to \infty$, $f''(x) \to 0$. There is no constant $\mu > 0$ such that $f''(x) \ge \mu$ for all $x$.

---

## (b) $f(x) = \min\{x, 1-x\}$ over domain $\mathbb{R}$

**Answer: Concave**

This function is the minimum of two affine (linear) functions: $g(x) = x$ and $h(x) = 1-x$.

A known property of convex/concave functions is that the pointwise minimum of a set of concave functions is itself concave. Since affine functions are both convex and concave, $g(x)$ and $h(x)$ are concave. Therefore, their minimum $f(x)$ is **concave**.

Analytically/Geometrically:
The function looks like an inverted "V" with the peak at $x = 0.5$ (where $x = 1-x$).
For $x \le 0.5$, $f(x) = x$ (slope 1).
For $x > 0.5$, $f(x) = 1-x$ (slope -1).

It is not strictly concave because it is linear (affine segments) on $x < 0.5$ and $x > 0.5$.
It is not strongly concave for the same reason (second derivative is 0 almost everywhere).

---

## (c) McCulloch-Pitts neuron with ReLU: $f(x) = (\theta^T x)_+$ over domain $\mathbb{R}^n$

**Answer: Convex**

The function is given by $f(x) = \max\{0, \theta^T x\}$.
This is a composition of the function $g(y) = \max\{0, y\}$ (ReLU) and the affine mapping $h(x) = \theta^T x$.

1.  **Convexity of ReLU:** The function $g(y) = \max\{0, y\}$ is convex. It is the maximum of two convex functions ($y$ and $0$).
2.  **Composition Rule:** If $g: \mathbb{R} \to \mathbb{R}$ is convex and non-decreasing, and $h: \mathbb{R}^n \to \mathbb{R}$ is convex, then $g(h(x))$ is convex.
    Alternatively, a more general rule applies simply because the inner function is affine: If $g$ is convex and $h$ is affine, then $g(h(x))$ is convex.

Since $g(y)$ is convex and $x \mapsto \theta^T x$ is affine, the composition $f(x)$ is **convex**.

It is not strictly convex because on the half-space where $\theta^T x \le 0$, the function is constant ($f(x) = 0$), so it is "flat".

---

## (d) McCulloch-Pitts neuron with sigmoid: $f(x) = \text{sigm}(\theta^T x)$ over domain $\mathbb{R}^n$

**Answer: Neither convex nor concave**

Let $g(z) = \frac{1}{1+e^{-z}}$ be the sigmoid function. $f(x) = g(\theta^T x)$.
Since $\theta^T x$ is an affine mapping, the convexity of $f(x)$ depends entirely on the convexity of the scalar sigmoid function $g(z)$ along the line defined by $\theta$.

Let's examine $g''(z)$:
$$ g'(z) = g(z)(1 - g(z)) $$
$$ g''(z) = g'(z)(1 - g(z)) + g(z)(-g'(z)) = g(z)(1 - g(z))(1 - 2g(z)) $$

The sign of $g''(z)$ depends on the sign of $(1 - 2g(z))$.
Since $g(z) \in (0, 1)$:
*   If $g(z) < 1/2$ (which corresponds to $z < 0$), then $1 - 2g(z) > 0 \implies g''(z) > 0$. The function is convex in this region.
*   If $g(z) > 1/2$ (which corresponds to $z > 0$), then $1 - 2g(z) < 0 \implies g''(z) < 0$. The function is concave in this region.

Since the domain is $\mathbb{R}^n$ (and assuming $\theta \neq 0$), the argument $\theta^T x$ takes values in $(-\infty, \infty)$. The function transitions from convex to concave. Therefore, it is **neither convex nor concave** globally.

---

# Problem 4: Programming with CVX

## Part 1: Basic Resource Allocation [10 pts]

**Problem:** Minimize $\sum_{i=1}^{n} f_i(x_i)$ where $f_i(x_i) = -ix_i$, with $n=10$, $D=10$.

**Solution:** All resources are allocated to agent 10: $x_{10} = 10$, and $x_i = 0$ for $i < 10$.

**Explanation:** Since $f_i(x_i) = -ix_i$, the objective is $\sum_{i=1}^{10} -ix_i$. To minimize this (equivalently, maximize $\sum ix_i$), we should allocate all resources to the agent with the largest coefficient (agent 10). This is a linear program, and the optimal solution is at a vertex of the feasible region.

---

## Part 2: Fair Resource Allocation with Log Regularization [10 pts]

**Problem:** Minimize $\sum_{i=1}^{n} f_i(x_i) - \tau \sum_{i=1}^{n} \log x_i$

**Observations for three τ values:**

| τ | Allocation Pattern | Key Observation |
|---|-------------------|-----------------|
| 0.1 | Almost all to agent 10 | Weak fairness; allocation nearly identical to Part 1 |
| 1.0 | Gradual increase 1→10 | Moderate fairness; all agents receive resources, higher agents still favored |
| 5.0 | Nearly uniform | Strong fairness; resources well-distributed across all agents |

**Why the log term promotes fairness:**
- The log function has the property: $\log(x) \to -\infty$ as $x \to 0$
- This heavily penalizes giving any agent zero (or near-zero) resources
- The penalty forces the optimizer to spread resources across all agents

**Mathematical Insight:**
At the optimum, the KKT conditions give: $-i - \frac{\tau}{x_i} + \nu = 0$ (where $\nu$ is the multiplier for the budget constraint). This implies $x_i = \frac{\tau}{\nu - i}$, showing that larger τ leads to more uniform allocation.

**Trade-off:** Higher τ → more fairness, but lower overall "utility" (the original $-ix_i$ objective). This is exactly the fairness-efficiency trade-off seen in resource allocation systems.
