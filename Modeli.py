from dataclasses import dataclass, field

@dataclass
class Artikel:
    SKU: int = field(default=0)
    Style: str = field(default="")
    Manufacturer: str = field(default="")
    Name: str = field(default="")
    Colour: str = field(default="")
    Size: str = field(default="")
    Farbtyp: str = field(default="")
    GroessenTyp: str = field(default="")
    PCPack: int = field(default=0)
    PCCarton: int = field(defatul=0)
    WeightKG: int = field(default=0)
    Status: str = field(default="")
    EAN: int = field(default=0)
    ManufacturerSKU: str = field(default="")
