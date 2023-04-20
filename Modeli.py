from dataclasses import dataclass, field

@dataclass
class Artikel:
    SKU: int = field(default=0)
    Style: str = field(default="")
    Manufacturer: str = field(default="")