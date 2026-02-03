class PenguEats:
    def __init__(self):
        # Warenbestand mit Kategorisierung und Qualitätsmerkmalen (KI generierte Daten)
        self.inventory = {
            "Hering": {"quantity": 20, "freshness": 9, "category": "Kaltwasserfisch"},
            "Makrele": {"quantity": 10, "freshness": 8, "category": "Kaltwasserfisch"},
            "Krill": {"quantity": 50, "freshness": 10, "category": "Krustentiere"},
            "Lachs": {"quantity": 5, "freshness": 10, "category": "Premium-Segment"},
            "Tintenfisch": {"quantity": 8, "freshness": 7, "category": "Kopffüßer"},
        }

        # Rezeptur-Datenbank (KI generierte Daten)
        self.cookbook = {
            "Premium-Segment": {
                9: "Carpaccio vom Atlantik-Lachs mit Zitronen-Vinaigrette",
                7: "Lachsfilet in Blätterteigkruste",
                0: "Ragout von Edelfischen"
            },
            "Kaltwasserfisch": {
                9: "Sashimi-Variation mit frischem Ingwer",
                7: "In Meersalz gereifte Makrele vom Grill",
                5: "Traditioneller Fischeintopf nach nordischer Art",
                0: "Bouillabaisse von regionalen Fischsorten"
            },
            "Krustentiere": {
                9: "Krill-Cocktail an Plankton-Dressing",
                5: "Gebratene Krill-Puffer",
                0: "Krill-Essenz"
            },
            "Kopffüßer": {
                8: "Calamari im Tempura-Teigmantel",
                0: "Marinierter Tintenfisch auf mediterrane Art"
            },
            "Beilage": {
                9: "Frischer Algensalat mit geröstetem Sesam",
                0: "Getrocknete Algen-Variationen"
            }
        }

        self.balance = 100.0
        self.rent = 15.0
        self.species_consumption_stats = {}

    def apply_scientific_forecast(self, mean_supply, supply_risk):
        print(f"\n--- Strategische Analyse der Lieferkette (Supply Chain) ---")
        print(f"Erwarteter Lieferumfang: {mean_supply:.2f} Einheiten | Risiko-Level: {supply_risk:.2f}%")

        if supply_risk > 30:
            print(f"Status: Kritisches Lieferrisiko. Preisanpassung zur Nachfragesteuerung aktiv.")
            return 1.2
        else:
            print(f"Status: Lieferkette stabil. Standard-Preisliste aktiv.")
            return 1.0

    def process_order(self, species, fish_type, price_factor=1.0):
        print(f"\n[Auftrag] Anforderung durch Spezies '{species}': {fish_type}")

        if self._is_available(fish_type):
            self.inventory[fish_type]["quantity"] -= 1

            base_price = 25.0 if self.inventory[fish_type]["category"] == "Premium-Segment" else 15.0
            final_price = base_price * price_factor
            self.balance += final_price

            dish = self._create_gourmet_dish(fish_type)
            self._update_species_consumption(species, fish_type)

            print(f"Status: Bereitstellung von '{dish}' abgeschlossen.")
            print(f"Transaktion: {final_price:.2f} Einheiten verbucht. Saldo: {self.balance:.2f}")
        else:
            alternative = self._get_recommendation(fish_type)
            print(f"Status: {fish_type} nicht lieferbar. Alternative für {species}: {alternative}")

    def _update_species_consumption(self, species, fish_type):
        if species not in self.species_consumption_stats:
            self.species_consumption_stats[species] = []
        self.species_consumption_stats[species].append(fish_type)

    def _create_gourmet_dish(self, fish_type):
        item = self.inventory[fish_type]
        category = item["category"]
        freshness = item["freshness"]
        recipes = self.cookbook.get(category, self.cookbook["Kaltwasserfisch"])
        thresholds = sorted(recipes.keys(), reverse=True)
        for threshold in thresholds:
            if freshness >= threshold:
                return recipes[threshold]
        return "Fischgericht nach Tagesangebot"

    def _get_recommendation(self, out_of_stock_fish):
        category = self.inventory[out_of_stock_fish]["category"]
        for fish, data in self.inventory.items():
            if data["category"] == category and data["quantity"] > 0:
                return fish
        return max(self.inventory, key=lambda x: self.inventory[x]["quantity"])

    def _is_available(self, fish_type):
        return fish_type in self.inventory and self.inventory[fish_type]["quantity"] > 0

    def pay_bills(self):
        self.balance -= self.rent
        print(f"\n[Finanzen] Mietaufwand beglichen. Aktueller Saldo: {self.balance:.2f}")
