**1\. Zielbild der App**

FoxPost simuliert oder verarbeitet reale Paketlogistik-Daten mit Schwerpunkt auf:

* große Datenmengen (→ Begründung für Dask)  
* Batch- und ggf. Streaming-Verarbeitung  
* saubere Datenpipelines  
* reproduzierbare Analysen

### Kernfragen, die die App beantworten kann

* Wo befinden sich Pakete aktuell?  
* Wie lange dauern Lieferungen (pro Region / Fahrer / Hub)?  
* Wo entstehen Engpässe?  
* Wie kann man Routen oder Hubs datenbasiert optimieren?

**2\. Domänenmodell (fachliche Grundlage)**

**Zentrale Entitäten**

Package

* package\_id  
* weight  
* size  
* priority  
* sender  
* recipient

ShipmentEvent

* package\_id  
* timestamp  
* location\_id  
* status (created, picked\_up, in\_transit, delivered, delayed)

Location

* location\_id  
* type (hub, truck, destination)  
* lat  
* lon

Courier

* courier\_id  
* name  
* region

## **3\. Datenarchitektur (Data Engineering Fokus)**

### **Datenquellen**

* CSV / Parquet (Batch)  
* JSON Logs (Events)  
* Optional: Kafka-Simulation (später)

**Speicherformate**

| Zweck | Format |
| :---- | :---- |
| Rohdaten | CSV / JSON |
| Verarbeitung | Parquet |
| Aggregationen | Parquet |
| Ergebnisse | Parquet / CSV |

## **4\. Dask als zentrales Rückgrat**

### **Warum Dask?**

* Out-of-core Processing  
* Parallele Transformationen  
* Pandas-ähnliches API  
* Skalierbar vom Laptop → Cluster

### **Typische Dask-Objekte**

* dask.dataframe 		→ Events & Packages  
* dask.delayed			→ ETL-Steps  
* dask.distributed.Client	→ Monitoring & Skalierung

**5\. Projektstruktur**

foxpost/

* data/  
  * raw/  
  * processed/  
  * analytics/  
* foxpost/  
  * **init**.py  
  * config.py  
  * ingestion/  
    * load\_raw.py  
    * validate.py  
  * processing/  
    * clean\_events.py  
    * enrich\_events.py  
    * join\_packages.py  
  * analytics/  
    * delivery\_times.py  
    * bottlenecks.py  
    * route\_stats.py  
  * utils/  
    * dask\_client.py  
* scripts/  
  * run\_pipeline.py  
* requirements.txt  
* README.md

**6\. ETL-Pipeline**

### **Ingestion**

* Einlesen großer CSV/JSON-Dateien mit `dask.dataframe.read_*`  
* Schema-Validierung  
* Schreiben als Parquet

RAW \-\> PARQUET

### **Cleaning**

* Entfernen ungültiger Events  
* Timestamp-Normalisierung  
* Status-Normalisierung

### **Enrichment**

* Geo-Enrichment (Region aus Koordinaten)  
* SLA-Zuweisung je Pakettyp  
* Zeitfenster (Hour, Day, Week)

### **Aggregation**

* Lieferdauer pro Paket  
* Ø Lieferdauer pro Hub  
* Event-Counts pro Status

**7\. Typische Dask-Patterns (die du demonstrieren solltest)**

* `map_partitions`  
* `groupby().agg()`  
* Partitionierung nach Zeit (`set_index`)  
* Lazy Evaluation \+ `.compute()`  
* Persistieren von Zwischenergebnissen  
* Monitoring über Dask Dashboard

Das Projekt sollte bewusst zeigen, dass Pandas hier nicht mehr ausreicht.

**8\. Beispiel-Use-Cases (Outputs)**

### **Analytics**

* „Top 10 langsamste Hubs“  
* „Durchschnittliche Lieferzeit nach Region“  
* „Anteil verspäteter Pakete pro Tag“

### **Technische Metriken**

* Laufzeit Pandas vs. Dask (Benchmark\!)  
* Memory-Usage  
* Skalierung (1 → N Worker)

**9\. Erweiterungen (optional, aber stark)**

* Simulierter Datenstrom (Mini-Kafka)  
* Dask \+ ML (z. B. Lieferzeit-Prediction)  
* REST-API (FastAPI) für Abfragen  
* Deployment auf Local Cluster / Docker

**10\. Nächste konkrete Schritte (To-Do-Plan)**

1. Domänendaten generieren (Fake-Events, viele\!)  
2. Rohdaten als CSV/JSON speichern  
3. Dask-Client setup  
4. Ingestion → Parquet Pipeline  
5. Erste Aggregation (Lieferzeiten)  
6. Dashboard beobachten  
7. Dokumentieren, warum Dask nötig ist

**11\. Ergebnis**

Am Ende entsteht:

* eine realistische Data-Engineering-Pipeline  
* einen klaren Business-Case  
* ein skalierbares Python-Projekt  
* ein sehr gutes Portfolio-Projekt für Data Engineering

