import pymc as pm
import numpy as np
import arviz as az


class DemandMCMCModel:

    def __init__(self, observed_data):
        self.observed_data = np.array(observed_data, dtype=np.float64)
        self.model = None
        self.trace = None

    def build_model(self):
        with pm.Model() as model:

            lam = pm.Gamma(
                "lam",
                alpha=3.0,
                beta=0.2
            )

            pm.Poisson(
                "obs",
                mu=lam,
                observed=self.observed_data
            )

            self.model = model

    def run_mcmc(self, draws=1000, tune=1000, chains=4, seed=42):

        if self.model is None:
            raise ValueError("Model not built")

        with self.model:

            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                nuts_sampler="numpyro",
                random_seed=seed
            )

    def get_risk_metrics(self, threshold=13):

        posterior = self.trace.posterior["lam"].values.flatten()

        mean_val = float(np.mean(posterior))
        risk_val = float(np.mean(posterior < threshold) * 100)

        hdi = az.hdi(self.trace, hdi_prob=0.95).lam.values

        return mean_val, risk_val, hdi

    def get_trace(self):
        return self.trace