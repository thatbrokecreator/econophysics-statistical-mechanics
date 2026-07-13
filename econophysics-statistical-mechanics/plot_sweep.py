import numpy as np
import matplotlib.pyplot as plt

results = np.load("sweep_results.npy")
lambdas = sorted(set(results[:,0]))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

for lam in lambdas:
    mask = results[:,0] == lam
    alphas = results[mask, 1]
    ginis = results[mask, 2]
    gini_err = results[mask, 3]
    tails = results[mask, 4]
    tail_err = results[mask, 5]

    axes[0].errorbar(alphas, ginis, yerr=gini_err, marker='o', label=f"λ={lam}")
    axes[1].errorbar(alphas, tails, yerr=tail_err, marker='o', label=f"λ={lam}")

axes[0].set_xlabel("Preferential attachment bias (α)")
axes[0].set_ylabel("Gini coefficient")
axes[0].set_title("Inequality vs. Advantage Bias")
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].set_xlabel("Preferential attachment bias (α)")
axes[1].set_ylabel("Tail exponent (Hill estimator)")
axes[1].set_title("Tail Fatness vs. Advantage Bias")
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("results/parameter_sweep.png", dpi=150)
print("saved")