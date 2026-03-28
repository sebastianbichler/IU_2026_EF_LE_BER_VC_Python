from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ParcelRecord:
    parcel_id: int
    origin: str
    destination: str
    weight_kg: float
    shipped_at: datetime
    delivered_at: Optional[datetime]
    status: str