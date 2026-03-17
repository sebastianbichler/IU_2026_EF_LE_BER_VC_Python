import subprocess
from dataclasses import asdict
from typing import Dict, List

import pandas as pd
import streamlit as st

from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.domain.order import Order
from bear_honeyworks.services.inventory_service import InventoryService
from bear_honeyworks.services.order_service import OrderService
from bear_honeyworks.services.production_service import ProductionService


st.set_page_config(page_title="Bear Honeyworks", layout="wide")


def inventory_to_rows(inventory: Inventory) -> List[Dict[str, object]]:
    return [asdict(jar) for jar in inventory.jars]


def count_by_sort(inventory: Inventory) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for jar in inventory.jars:
        result[jar.sort] = result.get(jar.sort, 0) + 1
    return result


if "inventory" not in st.session_state:
    st.session_state.inventory = Inventory()

if "messages" not in st.session_state:
    st.session_state.messages = []

inventory: Inventory = st.session_state.inventory
messages: List[str] = st.session_state.messages

production_service = ProductionService()
inventory_service = InventoryService()
order_service = OrderService()

st.title("Bear Honeyworks")
st.caption("Demo zur statischen Typprüfung mit mypy in einer fiktiven Honigfabrik")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Honig produzieren")

    bear_name = st.text_input("Name des Bären", value="Balou")
    honey_sort = st.text_input("Honigsorte", value="Waldhonig")
    honey_weight = st.number_input("Gewicht pro Glas in kg", min_value=0.1, max_value=5.0, value=0.5, step=0.1)
    honey_quality = st.slider("Qualität", min_value=1, max_value=5, value=3)

    if st.button("Honig produzieren", use_container_width=True):
        bear = Bear(bear_name)

        # Normale Produktionslogik erzeugt HoneyJar
        jar = production_service.produce(bear, honey_sort)

        # Für die Demo überschreiben wir Gewicht/Qualität mit UI-Werten
        custom_jar = HoneyJar(
            weight=float(honey_weight),
            sort=jar.sort,
            quality=int(honey_quality),
        )

        inventory_service.store(inventory, custom_jar)
        messages.append(
            f"Produktion erfolgreich: 1 Glas {custom_jar.sort} wurde eingelagert."
        )
        st.success("Honig erfolgreich produziert und eingelagert.")

with col2:
    st.subheader("Bestellung verarbeiten")

    available_sorts = sorted({jar.sort for jar in inventory.jars})
    if not available_sorts:
        available_sorts = ["Waldhonig"]

    order_sort = st.selectbox("Sorte", options=available_sorts)
    order_quantity = st.number_input("Menge", min_value=1, max_value=100, value=1, step=1)

    if st.button("Bestellung ausführen", use_container_width=True):
        order = Order(sort=order_sort, quantity=int(order_quantity))
        matching_jars = [jar for jar in inventory.jars if jar.sort == order.sort]

        if len(matching_jars) < order.quantity:
            messages.append(
                f"Bestellung fehlgeschlagen: Nicht genug {order.sort} im Lager."
            )
            st.error("Zu wenig Bestand für diese Bestellung.")
        else:
            removed = 0
            remaining_jars: List[HoneyJar] = []
            for jar in inventory.jars:
                if jar.sort == order.sort and removed < order.quantity:
                    removed += 1
                    continue
                remaining_jars.append(jar)

            inventory.jars = remaining_jars

            ok = order_service.process_order(order, Inventory())
            # order_service wird hier nur thematisch eingebunden;
            # die sichtbare Demo-Logik läuft sortenspezifisch oben.

            messages.append(
                f"Bestellung erfolgreich: {order.quantity} Glas/Gläser {order.sort} ausgeliefert."
            )
            st.success("Bestellung erfolgreich verarbeitet.")

st.divider()

left, right = st.columns([1.4, 1])

with left:
    st.subheader("Lagerbestand")

    rows = inventory_to_rows(inventory)
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aktuell sind keine Honiggläser im Lager.")

with right:
    st.subheader("Übersicht")

    total_jars = len(inventory.jars)
    st.metric("Anzahl Glaeser", total_jars)

    sort_counts = count_by_sort(inventory)
    if sort_counts:
        chart_df = pd.DataFrame(
            {"Sorte": list(sort_counts.keys()), "Anzahl": list(sort_counts.values())}
        ).set_index("Sorte")
        st.bar_chart(chart_df)
    else:
        st.info("Noch keine Daten fuer die Auswertung vorhanden.")

st.divider()

st.subheader("Systemmeldungen")
if messages:
    for msg in reversed(messages[-8:]):
        st.write(f"- {msg}")
else:
    st.write("- Noch keine Aktionen ausgefuehrt.")

st.divider()

st.subheader("mypy Typpruefung")
if st.button("mypy ausfuehren"):
    result = subprocess.run(
        ["mypy"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        st.success("mypy meldet keine Fehler.")
        st.code(result.stdout if result.stdout else "Success: no issues found", language="text")
    else:
        st.error("mypy hat Fehler gefunden.")
        st.code(result.stdout + "\n" + result.stderr, language="text")