# Titel des Projekts

## 1. Einleitung
- Kontext des Projekts
- Zielsetzung
- Motivation

## 2. Wissenschaftliche Fragestellung
- Formulierte Forschungsfrage
- ggf. Hypothesen/Ausgangsannahmen

## 3. Theoretischer Hintergrund
- Relevante Konzepte (kurz)
- bisheriger Stand (Literatur, Methoden)
- begriffliche Abgrenzung

## 4. Methodik
- Beschreibung, wie der Code genutzt wird, um die Frage zu beantworten
- Datenbasis (synthetisch, real, generiert)
- Experimente / Testaufbau
- Messgrößen (Zeit, Speicher)

## 5. Implementierung
- Architekturüberblick
- Komponenten/Module
- Relevante Funktionen
- Besonderheiten (z. B. Lazy Evaluation vs. Eager)

## 6. Experimentelle Ausführung
- Beschreibung der durchgeführten Experimente
- Reproduzierbarkeit (auf macOs u. Windows ausführbar machen)
- Testfälle
- Kontrollgruppe für eager vs lazy - Stimmen die Daten? Daten mehrmals Testen

## 7. Ergebnisse
- Darstellung der erhobenen Daten
- Tabellen/Diagramme
- direkte Beobachtungen

## 8. Analyse & Diskussion
- Interpretation der Ergebnisse
- Rückbezug auf die Forschungsfrage
- Erklärung von Effekten
- Grenzen der Methode

## 9. Schlussfolgerung
- explizite Beantwortung der Frage
- Implikationen
- Ausblick / mögliche Weiterarbeit

## 10. Reflexion
- technisches & methodisches Learning
- Schwierigkeiten
- alternative Ansätze (nicht sicher)

## 11. Literaturverzeichnis
- Literatur
- Primärquellen
- Webquellen

## 12. Anhang

```mermaid
classDiagram
    %% Domänenklassen (basierend auf src/models.py)

    class Vegetable {
        -name : str
        -sort : str
        -plant_date : datetime
        -harvest_date : datetime
        -bed_id : int
        -shelf_life_days : int
        -amount : float
        +is_fresh(current_date : Optional[datetime]) : bool
        +freshness_ratio(current_date : Optional[datetime]) : float
    }

    class Bed {
        -id : int
        -name : str
        -size_m2 : float
    }

    class Customer {
        -name : str
        -species : str
        -subscription_type : str
        +__str__() : str
    }

    class SubscriptionBox {
        -customer : Customer
        -vegetables : List~Vegetable~
        -delivery_date : datetime
        -price : float
        +__str__() : str
    }

    class Order {
        -customer : Customer
        -vegetables : List~Vegetable~
        -delivery_date : datetime
        -price : float
        +__str__() : str
    }

    class Inventory {
        -items : List~Vegetable~
        +add_harvest(vegetable : Vegetable, amount : float)
        +get_fresh_items(current_date : Optional[datetime]) : Generator~Vegetable~
        +get_expired_items(current_date : Optional[datetime]) : Generator~Vegetable~
        +get_total_amount() : float
    }

    %% Beziehungen (aus `models.py` und globalen Daten in `main.py`)
    Bed "1" --> "*" Vegetable : contains
    Inventory "1" --> "*" Vegetable : stores
    Customer "1" --> "*" Order : places
    Customer "1" --> "*" SubscriptionBox : subscribes
    Order "*" --> "*" Vegetable : includes
    SubscriptionBox "*" --> "*" Vegetable : contains

    %% Application / Main module (globale Sammlungen und I/O-Funktionen in main.py)
    class Application {
        -vegetables : List~Vegetable~
        -beds : List~Bed~
        -customers : List~Customer~
        -inventory : Inventory
        -orders : List~Order~
        +save_data()
        +load_data()
        +add_vegetable()
        +create_subscription_box()
    }

    class Sensors {
        <<module>>
        +stream_soil_moisture(bed_id, base_moisture)
    }

    class Services {
        <<module>>
        +generate_subscription_boxes(...)
        +calculate_profit(orders, costs)
    }

    Application --> Bed : manages
    Application --> Inventory : uses
    Application --> Customer : manages
    Application --> Order : manages
    Services --> Application : used_by
    Sensors --> Application : feeds
```

- Codeauszüge
- Testprotokolle
- Screenshots
