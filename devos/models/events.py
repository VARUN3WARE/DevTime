from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    """A single flicker of productivity"""
    event_type: str
    file: str
    project: str
    timestamp: datetime = datetime.now()

@dataclass
class Session:
    """A long dive into the code sea"""
    project: str
    start_time: datetime = datetime.now()
    end_time: Optional[datetime] = None
    id: Optional[int] = None
