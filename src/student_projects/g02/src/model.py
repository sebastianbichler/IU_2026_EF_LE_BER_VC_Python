"""
Modul zur Definition der Datenstruktur (Model Layer).

Dieses Modul definiert das Schema für die Datenobjekte.
Es nutzt moderne Python-Features (Data Classes), um schlanken und wartbaren
Code zu gewährleisten. Es enthält keine Logik, sondern reine Datencontainer.
"""
from dataclasses import dataclass

@dataclass
class NutStash:
    """
    Repräsentiert ein einzelnes Nuss-Versteck als Datenobjekt.
    
    Attribute:
    - id (int): Eindeutige Identifikationsnummer
    - x, y (float): Geografische Koordinaten (0-100m) für die Kartierung
    - nut_type, tree_type (str): Kategorische Daten für statistische Auswertungen
    - amount (int): Anzahl der Nüsse (Basis für Zinseszins-Berechnung)
    - depth (float): Tiefe in cm (Entscheidender Faktor für Diebstahl-Risiko & Isolation)
    - expiration_date (str): ISO-Datum für Haltbarkeitsprüfungen
    """
    id: int
    x: float
    y: float
    nut_type: str
    tree_type: str        
    amount: int
    depth: float
    expiration_date: str

    def __repr__(self):
        """
        Liefert eine menschenlesbare String-Repräsentation des Objekts.
        Wird für Debugging-Zwecke und Logging verwendet.
        """
        return (f"🌰 #{self.id}: {self.amount}x {self.nut_type} (Baum: {self.tree_type}) "
                f"bei ({self.x:.1f}/{self.y:.1f}) | "
                f"{self.depth:.1f}cm tief | Haltbar: {self.expiration_date}")