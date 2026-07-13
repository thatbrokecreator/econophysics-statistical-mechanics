"""
Validate the simulated wealth distribution's tail exponent against
published empirical estimates for real-world US wealth data.

Reference values from the literature:
  - Klass et al. (2007): Pareto exponent ~1.49 for US wealth (Forbes 400 + survey data)
  - Recent capital income studies: wealth Pareto coefficient ~1.4
  - Gabaix (2009) survey: wealth tail exponent "rather stable, perhaps around 1.5"

We compare these to the tail exponent our simulation produces at various
alpha (preferential attachment) levels, using the standard Hill MLE estimator.
"""
import numpy as np
import matplotlib.pyplot as plt
from sweep import run_simulation, tail_exponent

REAL_WEALTH_PARETO_EXPONENT = 1.49  # Klass et al. 2007

num_agents = 2000
total_steps = 200_000
lambda_save = 0.25

alpha_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.7, 1.0]
tail_exponents = []

for alpha in alpha_values:
    w = run_simulation(num_agents, total_steps, lambda_save, alpha, seed=1)
    te = tail_exponent(w, top_frac=0.05)
    tail_exponents.append(te)
    print(f"alpha={alpha:.2f}  simulated tail exponent={te:.2f}  "
          f"(real-world benchmark: {REAL_WEALTH_PARETO_EXPONENT})")

# Find which alpha gets closest to the real-world value
diffs = [abs(t - REAL_WEALTH_PARETO_EXPONENT) for t in tail_exponents]
best_idx = int(np.argmin(diffs))
print(f"\nClosest match: alpha={alpha_values[best_idx]:.2f} "
      f"(tail exp={tail_exponents[best_idx]:.2f} vs real {REAL_WEALTH_PARETO_EXPONENT})")

# Plot
fig, ax = plt.subplots(figsize=(8,5.5))
ax.plot(alpha_values, tail_exponents, marker='o', color='steelblue', label='Simulated tail exponent')
ax.axhline(REAL_WEALTH_PARETO_EXPONENT, color='crimson', linestyle='--',
           label=f'Empirical US wealth (Klass et al. 2007): {REAL_WEALTH_PARETO_EXPONENT}')
ax.set_xlabel("Preferential attachment bias (α)")
ax.set_ylabel("Tail exponent (Hill estimator)")
ax.set_title("Simulated Tail Exponent vs. Empirical US Wealth Benchmark")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("results/real_data_validation.png", dpi=150)
print("saved plot")