from dataclasses import dataclass
from pylatex import Command

from pylatex.base_classes import LatexObject


@dataclass
class Quantity(LatexObject):
    value: float
    unit: str | Command

    def __post_init__(self):
        super().__init__()

    def dumps(self):
        if isinstance(self.unit, LatexObject):
            unit = self.unit.dumps()
        else:
            unit = self.unit
        return f"{self.value}{unit}"
