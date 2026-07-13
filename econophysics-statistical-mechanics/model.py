import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =====================================================================
# 1. PARAMETERS & INITIALIZATION
# =====================================================================
num_agents = 5000       # Size of the population
total_steps = 1500000   # Increased steps to let the asymmetric system stabilize
initial_wealth = 100.0  # Everyone starts equal
lambda_save = 0.25      # Base saving propensity (25%)

# The Preferential Attachment Factor (Realism Hook)
# 0.0 = pure random physics. 0.05 = wealthy agents have a 5% systematic edge.
alpha_advantage = 0.03  

wealth = np.full(num_agents, initial_wealth)

# =====================================================================
# 2. ASYMMETRIC TRANSACTION ENGINE
# =====================================================================
for step in range(total_steps):
    idx_i, idx_j = np.random.choice(num_agents, size=2, replace=False)
    
    w_i = wealth[idx_i]
    w_j = wealth[idx_j]
    
    # Total active wealth up for grabs in this collision
    combined_active = (1.0 - lambda_save) * (w_i + w_j)
    
    # Base random split
    epsilon = np.random.uniform(0, 1)
    
    # Introduce the advantage modifier based on who is richer
    if w_i > w_j and w_j > 0:
        # Agent i is richer; shift epsilon slightly in their favor
        ratio = w_i / w_j
        bias = alpha_advantage * np.tanh(ratio - 1) # Tanh keeps the bias bounded safely
        epsilon = np.clip(epsilon + bias, 0.01, 0.99)
    elif w_j > w_i and w_i > 0:
        # Agent j is richer; shift epsilon in their favor
        ratio = w_j / w_i
        bias = alpha_advantage * np.tanh(ratio - 1)
        epsilon = np.clip(epsilon - bias, 0.01, 0.99)
        
    # Calculate new wealth allocations
    w_i_new = lambda_save * w_i + epsilon * combined_active
    w_j_new = lambda_save * w_j + (1.0 - epsilon) * combined_active
    
    wealth[idx_i] = w_i_new
    wealth[idx_j] = w_j_new

# =====================================================================
# 3. ANALYSIS & FITTING
# =====================================================================
def boltzmann_gibbs(w, T):
    return (1.0 / T) * np.exp(-w / T)

counts, bin_edges = np.histogram(wealth, bins=50, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
popt, _ = curve_fit(boltzmann_gibbs, bin_centers[:25], counts[:25], p0=[initial_wealth]) # Fit to the lower/middle class range
fitted_temperature = popt[0]

# =====================================================================
# 4. PLOTTING THE BREAK POINT
# =====================================================================
plt.figure(figsize=(10, 6))

# Plot the simulation data
plt.hist(wealth, bins=60, density=True, alpha=0.6, color='#7a4a91', 
         edgecolor='black', label='Asymmetric Agent Simulation')

# Plot where the standard physical distribution EXPECTS the line to go
w_range = np.linspace(0, np.max(wealth), 500)
plt.plot(w_range, boltzmann_gibbs(w_range, fitted_temperature), color='#d9534f', 
         linewidth=2, linestyle='--', label='Theoretical Pure Physics Line')

plt.title(f"System Break: Preferential Attachment (α = {alpha_advantage})", fontsize=13, fontweight='bold')
plt.xlabel("Individual Wealth ($)", fontsize=11)
plt.ylabel("Probability Density P(w)", fontsize=11)
plt.yscale('log')
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=10)

plt.tight_layout()
