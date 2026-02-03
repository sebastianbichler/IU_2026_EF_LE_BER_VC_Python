import os
import logging
from core.restaurant import PenguEats
from utils.mcmc_model import perform_bayesian_analysis, get_risk_metrics

# Konfiguration des Backends für mathematische Berechnungen (Deaktivierung des C++ Compilers, da Probleme mit Anaconda-Installation)
os.environ["PYTENSOR_FLAGS"] = "cxx="
logging.getLogger("pytensor").setLevel(logging.ERROR)

def main():
    print("=== PENGUEATS ENTERPRISE: ANALYTICS & OPERATIONS ===")

    #Empirische Datenbasis
    delivery_history = [11, 13, 10, 14, 12, 11, 10, 15, 12, 11]

    print("\n[Phase 1] Initiierung der Bayesianischen Inferenz")
    try:
        #MCMC-Simulation
        trace = perform_bayesian_analysis(delivery_history)
        mean_rate, risk_level, hdi = get_risk_metrics(trace, threshold=13)

        print("\n[Phase 2] Analyseergebnisse der statistischen Modellierung:")
        print(f" - Erwartete durchschnittliche Fangrate: {mean_rate:.2f}")
        print(f" - Konfidenzintervall (95% HDI): {hdi}")
        print(f" - Wahrscheinlichkeit eines Versorgungsengpasses: {risk_level:.2f}%")

        management = PenguEats()

        # Kopplung der Analyseergebnisse
        price_multiplier = management.apply_scientific_forecast(mean_rate, risk_level)

        print("\n[Phase 3] Operatives Tagesgeschäft und Auftragsabwicklung:")

        # Simulation von Transaktionen basierend auf Spezies-Klassifizierung
        management.process_order("Eisbär", "Lachs", price_multiplier)
        management.process_order("Seehund", "Hering", price_multiplier)
        management.process_order("Walross", "Makrele", price_multiplier)
        management.process_order("Pinguin", "Krill", price_multiplier)

        management.pay_bills()

        print("\n[Status] Simulation erfolgreich abgeschlossen.")

    except Exception as e:
        print(f"\n[Kritischer Fehler] Systemabbruch während der Verarbeitung: {e}")


if __name__ == "__main__":
    main()
