import random
from datetime import datetime
from typing import Generator, Dict


def stream_soil_moisture(bed_id: int, base_moisture: float = 50.0) -> Generator[Dict, None, None]:
    while True:
        moisture = base_moisture + random.uniform(-10, 10)
        moisture = max(0, min(100, moisture))
        
        yield {
            "bed_id": bed_id,
            "moisture": round(moisture, 2),
            "timestamp": datetime.now()
        }


