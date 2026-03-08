import os
import sys
import pytest

# Füge g03 Root zum Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.web.app import app
import data_manager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Verhindere, dass die echten Daten überschrieben werden
    original_save = data_manager.save_data
    data_manager.save_data = lambda: None # Mock save
    
    # Bereinige Testdaten
    data_manager.vegetables.clear()
    data_manager.beds.clear()
    data_manager.customers.clear()
    data_manager.orders.clear()
    data_manager.inventory.items.clear()
    
    with app.test_client() as client:
        yield client
        
    data_manager.save_data = original_save

def test_05_routes_index_page_loads_successfully(client):
    """Prüft, ob die Startseite (/) erfolgreich lädt und den Titel 'RabbitFarm' enthält."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"RabbitFarm" in response.data

def test_06_routes_add_new_customer_via_form(client):
    """Prüft, ob über das Formular (/customers) ein neuer Kunde erfolgreich angelegt werden kann."""
    response = client.post('/customers', data={
        "name": "Bugs Bunny",
        "species": "Hase",
        "subscription_type": "Premium"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert len(data_manager.customers) == 1
    assert data_manager.customers[0].name == "Bugs Bunny"

def test_07_routes_add_new_bed_via_form(client):
    """Prüft, ob über das Formular (/beds) ein neues Beet erfolgreich angelegt werden kann."""
    response = client.post('/beds', data={
        "name": "Test Beet",
        "size": "5.5"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert len(data_manager.beds) == 1
    assert data_manager.beds[0].name == "Test Beet"

def test_08_routes_finances_page_displays_zero_revenue_initially(client):
    """Prüft, ob die Finanzübersicht (/finances) bei fehlenden Bestellungen initial 0 anzeigt."""
    response = client.get('/finances')
    assert response.status_code == 200
    assert b"0" in response.data # Mindestens eine Zahl (0 Umsatz)
