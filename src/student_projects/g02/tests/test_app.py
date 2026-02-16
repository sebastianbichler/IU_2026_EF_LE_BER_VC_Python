import unittest
from src.app import app

class TestWebRoutes(unittest.TestCase):
    
    def setUp(self):
        """Wird VOR jedem Test ausgeführt."""
        # Erstellt einen Test-Client der Flask-App
        self.app = app.test_client()
        # Aktiviert den Test-Modus (bessere Fehlermeldungen)
        self.app.testing = True

    def test_index_route(self):
        """Prüft: Ist das Dashboard (/) erreichbar?"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Optional: Prüfen, ob bestimmter Text im HTML enthalten ist
        self.assertIn(b"Sammys Secret Stash", response.data)

    def test_analyze_route(self):
        """Prüft: Funktioniert die Analyse-Seite (/analyze) ohne Absturz?"""
        response = self.app.get('/analyze')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()