# Fish Restaurant Analytics

Ein Python-basiertes Simulations- und Analysesystem für ein Fischrestaurant, inklusive Inventarverwaltung, Lieferungen, Bestellungen, Rechnungen und probabilistischer Modellierung mit PyMC.

---

## 📂 Projektstruktur

```text
pengueats/
│
├── src/
│   ├── app.py                  # Flask frontend
│   ├── main.py                 # CLI simulation entry point
│   ├── core/
│   │   └── penguEats.py        # Restaurant management logic
│   │
│   ├── models/
│   │   ├── fish.py
│   │   ├── supplier.py
│   │   ├── inventory_item.py
│   │   ├── delivery.py
│   │   ├── recipe.py
│   │   ├── menu_item.py
│   │   ├── order_item.py
│   │   ├── order.py
│   │   └── bill.py
│   │
│   ├── analytics/
│   │   ├── restaurant_analytics.py
│   │   └── supplier_reliability_model.py
│   │
│   ├── utils/
│   │   └── mcmc_model.py
│   │
│   └── templates/
│       └── index.html          # Flask UI
│
├── tests/
│   ├── models/
│   │   ├── test_fish.py
│   │   ├── test_supplier.py
│   │   ├── test_inventory_item.py
│   │   ├── test_delivery.py
│   │   ├── test_recipe.py
│   │   ├── test_menu_item.py
│   │   ├── test_order_item.py
│   │   ├── test_order.py
│   │   └── test_bill.py
│   │
│   ├── analytics/
│   │   ├── test_restaurant_analytics.py
│   │   └── test_supplier_reliability.py
│   │
│   └── core/
│       └── test_pengueats.py
│
└── docs/
    ├── PenguEats-Konzeptionsphase.pdf
    ├── restaurant_class_diagram.puml
    └── restaurant_class_diagram.svg
```

## Funktionen

Verwaltung von Fischarten mit Kosten und Lieferantendaten.

Nachverfolgung von Inventarartikeln mit Mengen und Ablaufdaten.

Verwaltung von Lieferungen von verschiedenen Lieferanten.

Erstellung von MenuItems und Bestellungen mit einzelnen Posten.

Generierung von Rechnungen mit Steuern.

Durchführung von Bayesianischen Analysen mit PyMC:

Prognose der Nachfrage

Lieferanten-Zuverlässigkeit

Wahrscheinlichkeit von Lagerengpässen

## Installation

Repository klonen:
```text
git clone https://github.com/yourusername/fish_restaurant.git
cd fish_restaurant
```

Abhängigkeiten installieren:

```text
pip install -r requirements.txt
```
Beispiel für requirements.txt: pymc, numpy, pandas, matplotlib

## Anwendung ausführen

Das Hauptskript starten:
```text
python main.py
```

Dies wird:

Restaurant, Inventar und Lieferanten initialisieren

Lieferungen und Bestellungen simulieren

MCMC-Analysen durchführen

## UML-Klassendiagramm

Wir Nutzen ein UML-Klassendiagramm zur Visualisierung der Systemstruktur:

Domain Layer: Fish, Supplier, InventoryItem, Delivery, MenuItem, OrderItem, Order, Bill, Restaurant

Analytics Layer: DemandModel, SupplierReliabilityModel, RestaurantAnalytics

Das UML-Klassendiagramm weißt die Beziehungen und Multiplikationen zwischen Klassen

Die Quell-Datei befindet sich in docs/restaurant_class_diagram.puml.

UML online ansehen auf https://www.plantuml.com (ohne Installation) oder durch öffnen des SVG's

## Analyseschicht (PyMC)

Die Projektdateien für probabilistische Analysen:

utils/mcmc_model.py → Nachfrageprognose pro Fischart

utils/supplier_mcmc.py → Modellierung der Lieferanten-Zuverlässigkeit

MCMC-Simulationen ermöglichen die Berechnung von:

Prognosen für die Nachfrage am nächsten Tag

Wahrscheinlichkeit von Lieferausfällen

Risiko von Lagerengpässen