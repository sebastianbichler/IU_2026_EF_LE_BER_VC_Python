import time
import numpy as np
import random
from .model import NutStash

class Analyzer:
    """
    Analysiert exakt die Daten, die sich aktuell in der Datenbank befinden.
    """

    @staticmethod
    def run_performance_comparison(stashes: list[NutStash]):
        """
        Nimmt die Verstecke und lässt Python vs. NumPy antreten.
        """
        if not stashes:
            return {"n": 0, "surv_py": 0, "surv_np": 0, "int_py": 0, "int_np": 0}

        # 1. Daten aus den Objekten extrahieren 
        # Wir simulieren wieder eine Kältewelle von -5 Grad für alle Orte
        n = len(stashes)
        temps_list = [-5.0] * n 
        
        depths_list = [s.depth for s in stashes]
        amounts_list = [s.amount for s in stashes]
        
        # NumPy Arrays erstellen
        depths_arr = np.array(depths_list)
        amounts_arr = np.array(amounts_list)
        temps_arr = np.array(temps_list)

        # --- DISZIPLIN 1: Winterprognose (Survival) ---
        
        # Methode A: Native Python Loop
        start_py = time.perf_counter()
        _ = Analyzer._survival_python(depths_list, amounts_list, temps_list)
        time_py_surv = time.perf_counter() - start_py

        # Methode B: NumPy Vektorisierung
        start_np = time.perf_counter()
        _ = Analyzer._survival_numpy_calc(depths_arr, amounts_arr, temps_arr)
        time_np_surv = time.perf_counter() - start_np

        # --- DISZIPLIN 2: Zinseszins (Interest) ---
        
        # Methode A: Native Python Loop
        start_py = time.perf_counter()
        _ = Analyzer._interest_python(amounts_list)
        time_py_int = time.perf_counter() - start_py

        # Methode B: NumPy Vektorisierung
        start_np = time.perf_counter()
        _ = Analyzer._interest_numpy_calc(amounts_arr)
        time_np_int = time.perf_counter() - start_np

        return {
            "n": n,
            "surv_py": time_py_surv,
            "surv_np": time_np_surv,
            "int_py": time_py_int,
            "int_np": time_np_int
        }

    # --- Hilfsfunktionen ---

    @staticmethod
    def _survival_python(depths, amounts, temps):
        results = []
        for i in range(len(depths)):
            loss = amounts[i] * 0.3 if depths[i] < 10.0 else 0
            real_stock = amounts[i] - loss
            cold_factor = abs(temps[i]) * 0.1
            insulation = depths[i] * 0.05
            need = max(1.0, 2.0 + cold_factor - insulation)
            results.append(real_stock >= need * 90)
        return results

    @staticmethod
    def _survival_numpy_calc(depths, amounts, temps):
        risk_mask = depths < 10.0
        losses = np.where(risk_mask, amounts * 0.3, 0)
        real_stocks = amounts - losses
        cold_factors = np.abs(temps) * 0.1
        insulations = depths * 0.05
        daily_needs = np.maximum(1.0, 2.0 + cold_factors - insulations)
        return real_stocks >= (daily_needs * 90)

    @staticmethod
    def _interest_python(amounts, years=5, rate=0.05):
        results = []
        factor = (1 + rate) ** years
        for amount in amounts:
            results.append(amount * factor)
        return results

    @staticmethod
    def _interest_numpy_calc(amounts, years=5, rate=0.05):
        return amounts * ((1 + rate) ** years)

    @staticmethod
    def analyze_real_data(stashes: list[NutStash]):
        """Berechnet die KPI-Werte für die Anzeige oben."""
        if not stashes:
            return False, 0, 0, 0, 0, 0, 0

        depths = np.array([s.depth for s in stashes])
        amounts = np.array([s.amount for s in stashes])
        
        avg_temp = -5.0
        
        # Diebstahl
        risk_mask = depths < 10.0
        probable_theft = np.floor(np.where(risk_mask, amounts * 0.3, 0))
        total_theft_loss = np.sum(probable_theft)
        real_stock = np.sum(amounts) - total_theft_loss

        # Bedarf
        cold_factor = abs(avg_temp) * 0.1
        insulation_factors = depths * 0.05
        daily_needs = np.maximum(1.0, 2.0 + cold_factor - insulation_factors)
        total_winter_need = np.sum(daily_needs) * 90

        is_enough = real_stock >= total_winter_need

        future_values = amounts * ((1.05) ** 5)
        total_future = np.sum(future_values)
        profit = total_future - np.sum(amounts)

        return is_enough, np.sum(amounts), total_theft_loss, real_stock, total_winter_need, total_future, profit