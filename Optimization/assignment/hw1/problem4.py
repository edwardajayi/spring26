"""
Problem 4: Programming with CVX (CVXPY)
Resource Allocation Optimization
"""

import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PART 1: Basic Resource Allocation
# ============================================================
# Problem: min sum_i f_i(x_i) where f_i(x_i) = -i * x_i
# Subject to: x_i >= 0, sum(x_i) <= D

print("=" * 60)
print("PART 1: Basic Resource Allocation")
print("=" * 60)

n = 10  # Number of agents
D = 10  # Total resource budget

# Define variables
x = cp.Variable(n)

# Define objective: f_i(x_i) = -i * x_i
# Note: i goes from 1 to n in the problem, so indices are (i+1)
coefficients = np.array([-(i + 1) for i in range(n)])  # [-1, -2, ..., -10]
objective = cp.Minimize(coefficients @ x)

# Define constraints
constraints = [
    x >= 0,                    # x_i >= 0 for all i
    cp.sum(x) <= D             # x_1 + x_2 + ... + x_n <= D
]

# Solve the problem
problem1 = cp.Problem(objective, constraints)
problem1.solve()

print(f"Status: {problem1.status}")
print(f"Optimal value: {problem1.value:.4f}")
print(f"Optimal x values:")
for i in range(n):
    print(f"  x_{i+1} = {x.value[i]:.4f}")

# Plot Part 1
fig1, ax1 = plt.subplots(figsize=(10, 6))
indices = np.arange(1, n + 1)
ax1.bar(indices, x.value, color='steelblue', edgecolor='black')
ax1.set_xlabel('Agent index i', fontsize=12)
ax1.set_ylabel('Allocated resource $x_i$', fontsize=12)
ax1.set_title('Part 1: Resource Allocation (f_i(x_i) = -ix_i)', fontsize=14)
ax1.set_xticks(indices)
ax1.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('problem4_part1.png', dpi=150)
plt.show()

print("\nObservation: All resources are allocated to agent 10 (highest coefficient)")
print("This makes sense because minimizing -10*x_10 means maximizing x_10.")

# ============================================================
# PART 2: Fair Resource Allocation with Log Barrier
# ============================================================
print("\n" + "=" * 60)
print("PART 2: Fair Resource Allocation with Log Regularization")
print("=" * 60)

# Problem: min sum_i f_i(x_i) - tau * sum_i log(x_i)
# The log term promotes spreading resources across all agents

# Try three different positive values of tau
tau_values = [0.1, 1.0, 5.0]
results = {}

fig2, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, tau in enumerate(tau_values):
    print(f"\n--- tau = {tau} ---")
    
    # Define variables (need to ensure x > 0 for log)
    x_fair = cp.Variable(n, pos=True)  # pos=True ensures x > 0
    
    # Objective: sum(-i*x_i) - tau * sum(log(x_i))
    objective_fair = cp.Minimize(coefficients @ x_fair - tau * cp.sum(cp.log(x_fair)))
    
    # Constraints
    constraints_fair = [
        cp.sum(x_fair) <= D
    ]
    
    # Solve
    problem2 = cp.Problem(objective_fair, constraints_fair)
    problem2.solve()
    
    print(f"Status: {problem2.status}")
    print(f"Optimal value: {problem2.value:.4f}")
    print(f"Optimal x values:")
    for i in range(n):
        print(f"  x_{i+1} = {x_fair.value[i]:.4f}")
    
    results[tau] = x_fair.value.copy()
    
    # Plot
    axes[idx].bar(indices, x_fair.value, color='coral', edgecolor='black')
    axes[idx].set_xlabel('Agent index i', fontsize=11)
    axes[idx].set_ylabel('Allocated resource $x_i$', fontsize=11)
    axes[idx].set_title(f'τ = {tau}', fontsize=13)
    axes[idx].set_xticks(indices)
    axes[idx].grid(axis='y', alpha=0.3)
    axes[idx].set_ylim(0, max(x_fair.value) * 1.1)

plt.suptitle('Part 2: Fair Resource Allocation with Log Regularization', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('problem4_part2.png', dpi=150)
plt.show()

# ============================================================
# COMBINED COMPARISON PLOT
# ============================================================
fig3, ax3 = plt.subplots(figsize=(12, 6))

width = 0.2
positions = np.arange(1, n + 1)

# Part 1 result
ax3.bar(positions - 1.5*width, x.value, width, label='No fairness (Part 1)', color='steelblue', edgecolor='black')

# Part 2 results for each tau
colors = ['lightcoral', 'coral', 'orangered']
for i, tau in enumerate(tau_values):
    offset = (-0.5 + i) * width
    ax3.bar(positions + offset, results[tau], width, label=f'τ = {tau}', color=colors[i], edgecolor='black')

ax3.set_xlabel('Agent index i', fontsize=12)
ax3.set_ylabel('Allocated resource $x_i$', fontsize=12)
ax3.set_title('Comparison: Resource Allocation with Different Fairness Levels', fontsize=14)
ax3.set_xticks(positions)
ax3.legend()
ax3.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('problem4_comparison.png', dpi=150)
plt.show()

# ============================================================
# ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS")
print("=" * 60)
print("""
Key Observations:

1. Part 1 (No Fairness):
   - All resources go to agent 10 (the agent with the largest coefficient).
   - This is because minimizing -10*x_10 is equivalent to maximizing x_10.
   - Result: Completely unfair allocation.

2. Part 2 (With Log Regularization):
   - The log term acts as a "fairness regularizer" because:
     * log(x) → -∞ as x → 0, so it penalizes giving any agent 0 resources
     * This forces resources to be spread among all agents
   
   - Effect of τ (tau):
     * Small τ (0.1): Fairness has weak effect, allocation still favors high-index agents
     * Medium τ (1.0): More balanced allocation, but still weighted toward higher indices
     * Large τ (5.0): Much more uniform distribution, fairness dominates
   
   - Trade-off: Higher τ means more fairness but less overall "utility" (the -ix_i objective)

3. Mathematical Insight:
   - The optimal solution balances: -i (marginal utility) = τ/x_i (marginal fairness cost)
   - This gives x_i ∝ τ/i at optimum (roughly), explaining the decreasing pattern with i
   
4. Practical Interpretation:
   - In resource allocation (bandwidth, money, etc.), the log fairness term
     ensures every participant receives some resources, similar to how
     "proportional fairness" works in networking.
""")
