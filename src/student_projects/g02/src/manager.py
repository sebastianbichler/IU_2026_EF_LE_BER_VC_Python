import json
import os
from .model import NutStash

class StashManager:
    def __init__(self):
        # Pfad zur Datei: g02/data/database.json
        self.data_dir = "data"
        self.file_path = os.path.join(self.data_dir, "database.json")
        
        self.stashes = []
        
        # Sicherstellen, dass der Ordner existiert
        self._ensure_directory()
        # Daten beim Start laden
        self.load_data()

    def _ensure_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def add_stash(self, stash: NutStash):
        self.stashes.append(stash)

    def get_stashes(self):
        return self.stashes

    def save_data(self):
        """Speichert die Liste als JSON."""
        print(f"Speichere {len(self.stashes)} Verstecke nach: {self.file_path}")
        
        data_to_save = []
        for s in self.stashes:
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
                json.dump(data_to_save, f, indent=4)
            print("Speichern erfolgreich.")
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def load_data(self):
        """Lädt Daten und fängt Fehler bei alten/kaputten Dateien ab."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            self.stashes = []
            for item in raw_data:
                t_type = item.get('tree_type', 'Unbekannter Baum')
                
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
            print(f"📂 {len(self.stashes)} Verstecke geladen.")
            
        except Exception as e:
            print(f"⚠️ Fehler beim Laden (Datei evtl. korrupt/alt): {e}")
            # Im Fehlerfall starten wir lieber leer, statt abzustürzen
            self.stashes = []