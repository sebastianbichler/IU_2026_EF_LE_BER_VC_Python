import pymc as pm
import numpy as np
import arviz as az


class SupplierReliabilityModel:

    def __init__(self, successes, total):

        self.successes = successes
        self.total = total

        self.model = None
        self.trace = None

    def build_model(self):

        with pm.Model() as model:

            reliability = pm.Beta(
                "reliability",
                alpha=2,
                beta=2
            )

            pm.Binomial(
                "deliveries",
                n=self.total,
                p=reliability,
                observed=self.successes
            )

            self.model = model

    def run_mcmc(self, draws=1000, tune=1000, chains=4):

        with self.model:

            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                nuts_sampler="numpyro"
            )

    def get_reliability(self):

        posterior = self.trace.posterior["reliability"].values.flatten()

        mean = float(np.mean(posterior))
        hdi = az.hdi(self.trace, hdi_prob=0.95).reliability.values

        return mean, hdi