"""
Parameter sweep for the preferential-attachment wealth exchange model.

For each (lambda_save, alpha_advantage) pair, run the simulation to
equilibrium and measure:
  - Gini coefficient (inequality)
  - Tail exponent (power-law fit to the top 10% of wealth holders)

This lets us see how savings behavior and preferential attachment
interact to shape the resulting wealth distribution.
"""
import numpy as np

def run_simulation(num_agents, total_steps, lambda_save, alpha_advantage, seed):
    rng = np.random.default_rng(seed)
    wealth = np.full(num_agents, 100.0)

    for step in range(total_steps):
        idx_i, idx_j = rng.choice(num_agents, size=2, replace=False)
        w_i, w_j = wealth[idx_i], wealth[idx_j]
        combined_active = (1.0 - lambda_save) * (w_i + w_j)
        epsilon = rng.uniform(0, 1)

        if w_i > w_j and w_j > 0:
            bias = alpha_advantage * np.tanh((w_i / w_j) - 1)
            epsilon = np.clip(epsilon + bias, 0.01, 0.99)
        elif w_j > w_i and w_i > 0:
            bias = alpha_advantage * np.tanh((w_j / w_i) - 1)
            epsilon = np.clip(epsilon - bias, 0.01, 0.99)

        wealth[idx_i] = lambda_save * w_i + epsilon * combined_active
        wealth[idx_j] = lambda_save * w_j + (1.0 - epsilon) * combined_active

    return wealth


def gini_coefficient(wealth):
    x = np.sort(wealth)
    n = len(x)
    cum = np.cumsum(x)
    return (n + 1 - 2 * np.sum(cum) / cum[-1]) / n


def tail_exponent(wealth, top_frac=0.10):
    """
    Rough power-law tail exponent via the Hill estimator on the top
    `top_frac` of the distribution. Smaller exponent = fatter tail
    (more extreme inequality at the top).
    """
    x = np.sort(wealth)[::-1]
    k = max(int(len(x) * top_frac), 10)
    top = x[:k]
    xmin = x[k - 1]
    logs = np.log(top / xmin)
    alpha_hat = 1 + k / np.sum(logs[logs > 0])
    return alpha_hat


if __name__ == "__main__":
    num_agents = 1000
    total_steps = 100_000

    lambda_values = [0.1, 0.25, 0.4]
    alpha_values = [0.0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.18, 0.25]

    results = []
    for lam in lambda_values:
        for alpha in alpha_values:
            ginis = []
            tails = []
            for trial in range(3):  # 3 trials per setting to reduce noise
                w = run_simulation(num_agents, total_steps, lam, alpha, seed=trial)
                ginis.append(gini_coefficient(w))
                tails.append(tail_exponent(w))
            g_mean, g_std = np.mean(ginis), np.std(ginis)
            t_mean, t_std = np.mean(tails), np.std(tails)
            results.append((lam, alpha, g_mean, g_std, t_mean, t_std))
            print(f"lambda={lam:.2f} alpha={alpha:.3f} "
                  f"Gini={g_mean:.3f}+-{g_std:.3f} "
                  f"TailExp={t_mean:.2f}+-{t_std:.2f}")

    np.save("sweep_results.npy", np.array(results))
    print("\nSaved results to sweep_results.npy")