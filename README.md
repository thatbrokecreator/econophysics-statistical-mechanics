# Econophysics Statistical Mechanics Framework

A calibration engine that applies statistical mechanics to asset exchange dynamics — modeling
an economy as a closed thermodynamic system where currency units behave like energy quanta
colliding between particles.

## Core Idea

Purely randomized wealth exchange, under strict conservation laws, converges on a
Boltzmann-Gibbs (exponential) distribution — the same math that describes energy distribution
among gas molecules. But real-world wealth data shows heavy power-law tails, not clean
exponentials. This project shows why: introducing a systemic advantage for wealthier agents
breaks the thermal equilibrium and reproduces those empirical power-law tails.

## Theoretical Methodology

**Phase I — Thermal Analogue (Conservation Laws)**
Two randomly chosen agents exchange wealth via a kinetic-collision model. Total wealth is
strictly conserved (first law of thermodynamics). A savings propensity λ controls how much
capital is "active" in each transaction:

ΔW = (1 - λ)(w_i + w_j)

This converges to the equilibrium distribution:

P(w) = (1/T) × e^(-w/T)

**Phase II — Preferential Attachment (Asymmetric Advantage)**
A bias parameter α gives wealthier agents a systemic edge in transaction outcomes, scaled by a
bounded tanh function (to avoid runaway overflow at large wealth differentials):

Bias = α × tanh((w_rich / w_poor) - 1)

This structural break produces the heavy-tailed, power-law wealth distributions seen in real
economic data.

## Files

| File | Purpose | Output |
|---|---|---|
| `model.py` | Runs the dual-stage transaction loop (pure physics vs. advantage scaling) | `asymmetric_plot.png` |
| `validate.py` | Runs 200,000 transactions and benchmarks simulated wealth distribution against an empirical baseline | `validation_plot.png` |

## Installation & Execution

```bash
pip install numpy matplotlib
python model.py
python validate.py
```

## Next Steps / Possible Extensions

- **Dynamic savings propensities:** make λ vary by wealth, so low-income agents save less than
  wealthy agents — closer to real consumption behavior.
- **Taxation & redistribution:** add a tax on transactions feeding a public pool redistributed
  to the population, to study its effect on the Gini coefficient.
