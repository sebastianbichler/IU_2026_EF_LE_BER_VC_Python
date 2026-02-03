import pymc as pm
import numpy as np
import arviz as az


def perform_bayesian_analysis(observed_data):
    """
    Bayesianische Analyse mit JAX/Numpyro.
    Maximale Performance auf Windows OHNE C++ Compiler.
    """
    # Daten für JAX vorbereiten
    data = np.array(observed_data, dtype=np.float64)

    with pm.Model() as model:
        # Ein Gamma-Prior ist statistisch sauber für Raten
        lam = pm.Gamma("lam", alpha=3.0, beta=0.2)
        obs = pm.Poisson("obs", mu=lam, observed=data)

        # JAX-basierten Sampler weil Anaconda probleme macht
        # numpyro effizient und braucht kein g++
        trace = pm.sample(
            draws=1000,
            tune=1000,
            chains=4,
            nuts_sampler="numpyro",
            random_seed=42
        )
    return trace


def get_risk_metrics(trace, threshold=13):
    """Extraktion der Ergebnisse."""
    posterior = trace.posterior["lam"].values.flatten()
    mean_val = np.mean(posterior)
    risk_val = np.mean(posterior < threshold) * 100
    hdi = az.hdi(trace, hdi_prob=0.95).lam.values

    return mean_val, risk_val, hdi
