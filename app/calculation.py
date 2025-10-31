"""Calculation data structure."""
from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime


@dataclass
class Calculation:
    operation: str
    operands: List[float]
    result: float
    timestamp: str

    @classmethod
    def create(cls, operation: str, operands, result) -> "Calculation":
        return cls(operation=operation, operands=list(operands), result=result, timestamp=datetime.utcnow().isoformat())

    def to_dict(self):
        d = asdict(self)
        d["operands"] = ";".join(str(x) for x in self.operands)
        return d
