from dataclasses import dataclass

__all__ = ["Bbox"]


@dataclass
class Bbox:
    x: float
    y: float
    w: float
    h: float
