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

@dataclass
class StyleList:
    Style: str = field(default="")
    Name1: str = field(default="")
    Name2: str = field(default="")
    MaterialDescription: str = field(default="")
    ProductDescription: str = field(default="")
    CataloguePage: str = field(default="")
    OrientationPrice: str = field(default="")
    ItemCode: int = field(default=0)
    Origin: str = field(default="")
    Status: str = field(default="")
    Categories: str = field(default="")


@dataclass
class Colour:
    ColourCode: int = field(default=0)
    ColourName: str = field(default="")
    SortOrder: int = field(default=0)

@dataclass
class Size:
    SizeCode: str = field(default="")
    SizeName: str = field(default="")

@dataclass
class ColourTemplate:
    ManufName: str = field(default="")
    ManufCode: str = field(default="")
    ColourName: str = field(default="")
    CMYK: str = field(default="")
    RGB: str = field(default="")


