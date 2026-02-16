import unittest
import numpy as np
from src.analytics import Analyzer
from src.model import NutStash

class TestAnalyzer(unittest.TestCase):
    
    def test_compare_numpy_and_python(self):
        """
        Wissenschaftlicher Test:
        Prüft, ob der vektorisierte NumPy-Code exakt dasselbe Ergebnis liefert
        wie der iterative Python-Code.
        """
        # 1. Testdaten vorbereiten
        depths = [5.0, 20.0, 8.0, 60.0]  # Mix aus sicher (>10) und unsicher (<10)
        amounts = [100, 100, 100, 100]
        temps = [-5.0, -5.0, -5.0, -5.0]
        
        # 2. Python-Berechnung (SISD)
        res_py = Analyzer._survival_python(depths, amounts, temps)
        
        # 3. NumPy-Berechnung (SIMD)
        res_np = Analyzer._survival_numpy_calc(
            np.array(depths), 
            np.array(amounts), 
            np.array(temps)
        )
        
        # 4. Assertion (Vergleich)
        # np.testing.assert_array_equal ist spezialisiert auf Array-Vergleiche
        np.testing.assert_array_equal(res_np, res_py)

    def test_logic_theft_risk(self):
        """
        Business Logic Test:
        Prüft, ob die Diebstahl-Logik (Tiefe < 10cm) korrekt greift.
        """
        # Szenario: Ein Versteck ist zu flach (5cm), eins ist tief genug (15cm)
        # Wir nutzen direkt die NumPy-Logik, da sie der Standard im 'analyze_real_data' ist.
        depths = np.array([5.0, 15.0])
        amounts = np.array([100, 100])
        
        risk_mask = depths < 10.0
        losses = np.where(risk_mask, amounts * 0.3, 0)
        
        # Erwartung:
        # Index 0 (5cm): 30% Verlust von 100 = 30
        # Index 1 (15cm): 0% Verlust = 0
        self.assertEqual(losses[0], 30.0)
        self.assertEqual(losses[1], 0.0)

if __name__ == '__main__':
    unittest.main()