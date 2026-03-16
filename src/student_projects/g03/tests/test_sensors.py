"""Unit-Tests für sensors.py – Bodenfeuchte-Streamgenerator."""

from itertools import islice
from datetime import datetime

from sensors import stream_soil_moisture


class TestStreamSoilMoisture:
    """Tests für stream_soil_moisture()."""

    def test_returns_generator(self):
        """Liefert einen Generator zurück."""
        import types

        gen = stream_soil_moisture(bed_id=1)
        assert isinstance(gen, types.GeneratorType)

    def test_yields_valid_dict(self):
        """Jeder gelieferte Wert stellt ein Dictionary mit bed_id, moisture und timestamp dar."""
        gen = stream_soil_moisture(bed_id=42)
        reading = next(gen)

        assert isinstance(reading, dict)
        assert "bed_id" in reading
        assert "moisture" in reading
        assert "timestamp" in reading

    def test_bed_id_matches(self):
        """Die bed_id in jedem Eintrag entspricht der Eingabe."""
        gen = stream_soil_moisture(bed_id=7)
        reading = next(gen)
        assert reading["bed_id"] == 7

    def test_moisture_range(self):
        """Die Feuchtigkeit bewegt sich zwischen 0 und 100."""
        gen = stream_soil_moisture(bed_id=1, base_moisture=50.0)
        readings = list(islice(gen, 100))

        for r in readings:
            assert 0.0 <= r["moisture"] <= 100.0

    def test_timestamp_type(self):
        """Der Zeitstempel ist ein Datetime-Objekt."""
        gen = stream_soil_moisture(bed_id=1)
        reading = next(gen)
        assert isinstance(reading["timestamp"], datetime)

    def test_multiple_readings(self):
        """Erzeugt problemlos viele Messwerte hintereinander."""
        gen = stream_soil_moisture(bed_id=1)
        readings = list(islice(gen, 1000))
        assert len(readings) == 1000

    def test_base_moisture_influence(self):
        """Die Messwerte bündeln sich um den Basiswert (base_moisture)."""
        gen = stream_soil_moisture(bed_id=1, base_moisture=80.0)
        readings = list(islice(gen, 200))
        avg = sum(r["moisture"] for r in readings) / len(readings)
        assert 65.0 <= avg <= 95.0
