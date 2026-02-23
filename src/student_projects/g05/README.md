# Fish Restaurant Analytics

Ein Python-basiertes Simulations- und Analysesystem für ein Fischrestaurant, inklusive Inventarverwaltung, Lieferungen, Bestellungen, Rechnungen und probabilistischer Modellierung mit PyMC.

---

## 📂 Projektstruktur

```text
fish_restaurant/
│
├── models/
│   ├── fish.py
│   ├── supplier.py
│   ├── inventory.py
│   ├── delivery.py
│   ├── menu_item.py
│   ├── order_item.py
│   ├── order.py
│   └── bill.py
│
├── utils/
│   ├── mcmc_model.py
│   └── supplier_mcmc.py
│
├── restaurant.py
├── main.py
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