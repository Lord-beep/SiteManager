from dataclasses import dataclass
from typing import Optional


@dataclass
class Site:
    id: Optional[int]
    name: str
    platform: str
    interval_minutes: int
    active: bool
    last_execution: Optional[str] = None
    domain: Optional[str] = None