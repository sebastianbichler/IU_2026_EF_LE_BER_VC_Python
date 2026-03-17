# Hauptdatei für die Bear Honeyworks Demo-Anwendung, die eine einfache Honigfabrik simuliert. Diese Anwendung ermöglicht es Benutzern, Honig zu produzieren, Bestellungen zu verarbeiten und den Lagerbestand sowie die Bestellhistorie anzuzeigen. Die Anwendung ist in Streamlit implementiert und nutzt verschiedene Domänenmodelle, Repositories und Services, um die Geschäftslogik zu kapseln und die Datenpersistenz zu gewährleisten. Zusätzlich gibt es eine Integration mit mypy, um die statische Typprüfung direkt aus der UI heraus durchzuführen.
import subprocess
from dataclasses import asdict
from typing import Dict, List

import pandas as pd
import streamlit as st

# Domänenmodelle
from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.domain.order import Order

# Repositories (Persistenz / JSON)
from bear_honeyworks.repositories.inventory_repository import InventoryRepository
from bear_honeyworks.repositories.order_repository import OrderRepository

# Geschäftslogik
from bear_honeyworks.services.inventory_service import InventoryService
from bear_honeyworks.services.order_service import OrderService
from bear_honeyworks.services.production_service import ProductionService


# Streamlit Grundkonfiguration
st.set_page_config(page_title="Bear Honeyworks", layout="wide")


# Hilfsfunktionen für Darstellung und Auswertung
def inventory_to_rows(inventory: Inventory) -> List[Dict[str, object]]:
    # Wandelt die Honiggläser im Inventar in eine Liste von Dictionaries um, die für die Anzeige in einem DataFrame geeignet ist.
    return [asdict(jar) for jar in inventory.jars]


def orders_to_rows(orders: List[Order]) -> List[Dict[str, object]]:
    # Wandelt die Bestellungen in Tabellenzeilen für die Anzeige um.
    return [asdict(order) for order in orders]


def count_by_sort(inventory: Inventory) -> Dict[str, int]:
    # Zählt die Anzahl der Honiggläser pro Sorte, basierend auf dem sort-Attribut der Gläser.
    result: Dict[str, int] = {}
    for jar in inventory.jars:
        result[jar.sort] = result.get(jar.sort, 0) + 1
    return result


def count_by_bear(inventory: Inventory) -> Dict[str, int]:
    # Zählt die Anzahl der Honiggläser pro Bär, basierend auf dem bear_name-Attribut der Gläser.
    result: Dict[str, int] = {}
    for jar in inventory.jars:
        result[jar.bear_name] = result.get(jar.bear_name, 0) + 1
    return result


def weight_by_bear(inventory: Inventory) -> Dict[str, float]:
    # Berechnet die Gesamtmenge an Honig (in kg) pro Bär, indem das Gewicht der Gläser summiert wird.
    result: Dict[str, float] = {}
    for jar in inventory.jars:
        result[jar.bear_name] = result.get(jar.bear_name, 0.0) + jar.weight
    return result


def reload_data() -> None:
    # Lädt die Daten aus den JSON-Dateien neu und aktualisiert den Session State entsprechend, um sicherzustellen, dass die Anwendung mit den aktuellen Daten arbeitet.
    fresh_inventory = Inventory()
    fresh_inventory.jars = inv_repo.load()
    st.session_state.inventory = fresh_inventory
    st.session_state.orders = order_repo.load()


def reset_demo() -> None:
    # Setzt die Demo zurück, indem er ein leeres Inventar und eine leere Bestellliste erstellt, diese im Session State speichert und die JSON-Dateien entsprechend aktualisiert.
    empty_inventory = Inventory()
    st.session_state.inventory = empty_inventory
    st.session_state.orders = []
    st.session_state.messages = []

    inv_repo.save([])
    order_repo.save([])


# Repositories initialisieren
inv_repo = InventoryRepository()
order_repo = OrderRepository()


# Session State initialisieren
if "inventory" not in st.session_state:
    initial_inventory = Inventory()
    initial_inventory.jars = inv_repo.load()
    st.session_state.inventory = initial_inventory

if "orders" not in st.session_state:
    st.session_state.orders = order_repo.load()

if "messages" not in st.session_state:
    st.session_state.messages = []


# Zugriff auf gespeicherte Daten
inventory: Inventory = st.session_state.inventory
orders: List[Order] = st.session_state.orders
messages: List[str] = st.session_state.messages


# Services initialisieren
production_service = ProductionService()
inventory_service = InventoryService()
order_service = OrderService()


# UI Header
st.title("Bear Honeyworks")
st.caption("Demo zur statischen Typprüfung mit mypy in einer fiktiven Honigfabrik")


# Steuerungsbereich
control_col1, control_col2, control_col3 = st.columns([1, 1, 1])

with control_col1:
    if st.button("Daten neu laden", width="stretch"):
        reload_data()
        st.success("Daten wurden aus den JSON-Dateien neu geladen.")

with control_col2:
    if st.button("Demo zurücksetzen", width="stretch"):
        reset_demo()
        st.success("Demo wurde vollständig zurückgesetzt.")

with control_col3:
    st.info("JSON-Dateien: data/inventory.json und data/orders.json")


# Zwei Spalten: Produktion | Bestellung
col1, col2 = st.columns([1, 1])


# PRODUKTION
with col1:
    st.subheader("Honig produzieren")

    bear_name = st.text_input("Name des Bären", value="Balou")
    honey_sort = st.text_input("Honigsorte", value="Waldhonig")
    honey_weight = st.number_input(
        "Gewicht pro Glas in kg",
        min_value=0.1,
        max_value=5.0,
        value=0.5,
        step=0.1,
    )
    honey_quality = st.slider("Qualität", min_value=1, max_value=5, value=3)

    if st.button("Honig produzieren", width="stretch"):
        # Einfache Validierung
        if not bear_name.strip():
            st.error("Der Name des Bären darf nicht leer sein.")
        elif not honey_sort.strip():
            st.error("Die Honigsorte darf nicht leer sein.")
        else:
            bear = Bear(bear_name.strip())

            # Produktion über Service
            jar = production_service.produce(bear, honey_sort.strip())

            # UI-Werte für Demo übernehmen
            custom_jar = HoneyJar(
                weight=float(honey_weight),
                sort=jar.sort,
                quality=int(honey_quality),
                bear_name=bear.name,
            )

            inventory_service.store(inventory, custom_jar)
            inv_repo.save(inventory.jars)

            messages.append(
                f"Produktion: {bear.name} hat 1 Glas {custom_jar.sort} erzeugt "
                f"(Qualität {custom_jar.quality}, {custom_jar.weight} kg)"
            )
            st.success("Honig erfolgreich produziert und eingelagert.")


# BESTELLUNG
with col2:
    st.subheader("Bestellung verarbeiten")

    available_sorts = sorted({jar.sort for jar in inventory.jars})
    if not available_sorts:
        available_sorts = ["Waldhonig"]

    order_sort = st.selectbox("Sorte", options=available_sorts)
    order_quantity = st.number_input(
        "Menge",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
    )

    if st.button("Bestellung ausführen", width="stretch"):
        order = Order(sort=order_sort, quantity=int(order_quantity))
        delivered_jars = order_service.process_order(order, inventory)

        if not delivered_jars:
            messages.append(
                f"Bestellung fehlgeschlagen: Nicht genug {order.sort} im Lager."
            )
            st.error("Zu wenig Bestand für diese Bestellung.")
        else:
            orders.append(order)
            inv_repo.save(inventory.jars)
            order_repo.save(orders)

            qualities = ", ".join(str(jar.quality) for jar in delivered_jars)
            bears = ", ".join(jar.bear_name for jar in delivered_jars)

            messages.append(
                f"Bestellung: {len(delivered_jars)}x {order.sort} ausgeliefert "
                f"(Qualität: {qualities}, von: {bears})"
            )
            st.success("Bestellung erfolgreich verarbeitet.")


# Lagerbestand und Auswertungen
st.divider()

left, right = st.columns([1.4, 1])

with left:
    st.subheader("Lagerbestand")

    rows = inventory_to_rows(inventory)
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, width="stretch")
    else:
        st.info("Aktuell sind keine Honiggläser im Lager.")

with right:
    st.subheader("Übersicht")

    st.metric("Anzahl Gläser", len(inventory.jars))

    sort_counts = count_by_sort(inventory)
    if sort_counts:
        st.write("**Gläser pro Sorte**")
        st.bar_chart(pd.DataFrame.from_dict(sort_counts, orient="index"))

    bear_counts = count_by_bear(inventory)
    if bear_counts:
        st.write("**Gläser pro Bär**")
        st.bar_chart(pd.DataFrame.from_dict(bear_counts, orient="index"))

    bear_weights = weight_by_bear(inventory)
    if bear_weights:
        st.write("**Honigmenge pro Bär (kg)**")
        st.bar_chart(pd.DataFrame.from_dict(bear_weights, orient="index"))


# Bestellhistorie
st.divider()

st.subheader("Bestellhistorie")

order_rows = orders_to_rows(orders)
if order_rows:
    order_df = pd.DataFrame(order_rows)
    st.dataframe(order_df, width="stretch")
else:
    st.info("Es wurden noch keine Bestellungen gespeichert.")


# Systemmeldungen
st.divider()

st.subheader("Systemmeldungen")
if messages:
    for msg in reversed(messages[-8:]):
        st.write(f"- {msg}")
else:
    st.write("- Noch keine Aktionen ausgeführt.")


# mypy Integration
st.divider()

st.subheader("mypy Typprüfung")

if st.button("mypy ausführen", width="stretch"):
    result = subprocess.run(
        ["mypy"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        st.success("mypy meldet keine Fehler.")
        st.code(result.stdout or "Success: no issues found")
    else:
        st.error("mypy hat Fehler gefunden.")
        st.code(result.stdout + "\n" + result.stderr)