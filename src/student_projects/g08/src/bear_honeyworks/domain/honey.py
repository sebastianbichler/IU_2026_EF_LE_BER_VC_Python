from dataclasses import dataclass


@dataclass
class HoneyJar:
    weight: float  # in kg
    sort: str
    quality: int  # 1-5