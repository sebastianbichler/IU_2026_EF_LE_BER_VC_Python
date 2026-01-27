# Konzept – FoxExpress 🚚💨

## Leitfrage ❓

**„Leistungsanalyse von JIT-Kompilierungsstrategien in dynamischen Sprachen:  
Ein Vergleich zwischen methodenbasierter (Numba) und tracingbasierter (PyPy) JIT-Kompilierung bei unstrukturierten algorithmischen Workloads.“**

## Erläuterung 📌

Ziel des Projekts **„FoxExpress“** ist die Entwicklung einer vereinfachten Logistik-Software, mit der:

- Lieferungen erstellt und verwaltet werden können  
- kürzeste Lieferwege berechnet werden können  

Auf dieser Grundlage soll die Laufzeit identischer Algorithmen unter verschiedenen Python-Ausführungsumgebungen verglichen werden:

- **CPython**  
- **PyPy**  
- **Numba**  

Damit sollen Unterschiede zwischen:

- tracingbasierter JIT-Kompilierung (**PyPy**)  
- methodenbasierter JIT-Kompilierung (**Numba**)  

analysiert werden.

## Systemaufbau 🧩

Konzeptionell besteht **„FoxExpress“** aus:

- einem Modul zur Lieferverwaltung  
- einem Routing-Modul zur Berechnung kürzester Wege mittels **Dijkstra-Algorithmus**  
- einer grafischen Benutzeroberfläche  

Die Oberfläche wird mit **Streamlit** realisiert.

## Methodik ⏱️

Die Benchmark-Tests werden durchgeführt, indem:

- identische Routenberechnungen  
- mit festen Eingabedaten  
- wiederholt unter **CPython**, **PyPy** und **Numba**  

ausgeführt und die **Ausführungszeiten gemessen** werden.

Die Ergebnisse werden:

- statistisch ausgewertet  
- in der Oberfläche vergleichend dargestellt  

Als Methodik wird insgesamt ein **experimenteller Vergleich identischer Workloads** gewählt.
