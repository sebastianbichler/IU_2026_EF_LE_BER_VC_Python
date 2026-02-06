"""
Modul für die Datenhaltung 

Dieses Modul abstrahiert den Zugriff auf das Dateisystem.
Es sorgt dafür, dass die Daten (Nuss-Verstecke) dauerhaft in einer JSON-Datenbank
gespeichert werden und nach einem Programm-Neustart wieder verfügbar sind.
"""
import json
import os
from .model import NutStash

class StashManager:
    """
    Verwaltet die Lese- und Schreibzugriffe auf die JSON-Datenbank.
    
    Verantwortlichkeiten:
    - Serialisierung: Umwandlung von NutStash-Objekten in JSON-Format.
    - Deserialisierung: Umwandlung von JSON-Strings zurück in Objekte.
    - Fehlerbehandlung: Abfangen von Problemen bei fehlenden Dateien.
    """
    def __init__(self):
        """
        Initialisiert den Manager und bestimmt den Pfad zur Datenbankdatei.
        """
        # Pfad zur Datei: g02/data/database.json
        self.data_dir = "data"
        self.file_path = os.path.join(self.data_dir, "database.json")
        
        self.stashes = []
        
        # Sicherstellen, dass der Ordner existiert
        self._ensure_directory()

        # Daten beim Start laden
        self.load_data()

    def _ensure_directory(self):
        """
        Hilfsmethode: Prüft und erstellt bei Bedarf das Datenverzeichnis.
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def add_stash(self, stash: NutStash):
        """
        Fügt ein neues Versteck-Objekt zur Laufzeit-Liste hinzu.
        
        Args:
            stash (NutStash): Das neu erstellte Objekt.
        """
        self.stashes.append(stash)

    def get_stashes(self):
        """
        Getter für den Zugriff auf die aktuellen Daten im Arbeitsspeicher.
        """
        return self.stashes

    def save_data(self):
        """
        Serialisierung: Speichert den aktuellen Zustand in die JSON-Datei.
        
        Ablauf:
        1. Iteriert über alle Objekte im Speicher.
        2. Konvertiert jedes Objekt manuell in ein Dictionary (Mapping).
        3. Schreibt die Liste als JSON-String auf die Festplatte.
        """
        print(f"Speichere {len(self.stashes)} Verstecke nach: {self.file_path}")
        
        data_to_save = []
        for s in self.stashes:
            # Explizites Mapping der Attribute für die JSON-Kompatibilität
            data_to_save.append({
                "id": s.id,
                "x": s.x,
                "y": s.y,
                "nut_type": s.nut_type,
                "tree_type": s.tree_type,     
                "amount": s.amount,
                "depth": s.depth,
                "expiration_date": s.expiration_date
            })
            
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                # indent=4 sorgt für Lesbarkeit für Menschen
                json.dump(data_to_save, f, indent=4)
            print("Speichern erfolgreich.")
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def load_data(self):
        """
        Deserialisierung: Lädt Daten und rekonstruiert die Objekte.
        
        Beinhaltet 'Defensive Programming':
        - Prüft, ob die Datei existiert.
        - Fängt korrupte JSON-Daten ab, um Abstürze zu verhindern.
        - Setzt Standardwerte (Fallback), falls Felder (z.B. tree_type) in alten Daten fehlen.
        """
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            self.stashes = []
            for item in raw_data:
                # Fallback für Abwärtskompatibilität (falls alte Daten das Feld nicht haben)
                t_type = item.get('tree_type', 'Unbekannter Baum')
                
                # Instanziierung des NutStash Objekts aus den Rohdaten
                stash = NutStash(
                    id=item['id'],
                    x=item['x'],
                    y=item['y'],
                    nut_type=item['nut_type'],
                    tree_type=t_type,         
                    amount=item['amount'],
                    depth=item['depth'],
                    expiration_date=item['expiration_date']
                )
                self.stashes.append(stash)
            print(f"{len(self.stashes)} Verstecke geladen.")
            
        except Exception as e:
            print(f"Fehler beim Laden (Datei evtl. korrupt/alt): {e}")
            # Im Fehlerfall starten wir mit einer leeren Liste
            self.stashes = []