from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass
class Artikli:
    id: int = field(default=0)
    sku: str = field(default="")
    style: str = field(default="")
    manufacturer: str = field(default="")
    name: str = field(default="")
    colour: str = field(default="")
    size: str = field(default="")
    farbtyp: str = field(default="")
    goressentyp: str = field(default="")
    pcpack: int = field(default=0)
    pccarton: int = field(default=0)
    weightkg: str = field(default=0)
    status: str = field(default="")
    packshot: str = field(default="")
    ean: str = field(default="")
    manufacturersku: str = field(default="")

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Artikli':
        return cls(
            id=int(data.get('id', 0)),
            sku=data.get('sku', ''),
            style=data.get('style', ''),
            manufacturer=data.get('manufacturer', ''),
            name=data.get('name', ''),
            colour=data.get('colour', ''),
            size=data.get('size', ''),
            farbtyp=data.get('farbtyp', ''),
            goressentyp=data.get('goressentyp', ''),
            pcpack=int(data.get('pcpack', 0)),
            pccarton=int(data.get('pccarton', 0)),
            weightkg=data.get('weightkg', '0'),
            status=data.get('status', ''),
            packshot=data.get('packshot', ''),
            ean=data.get('ean', ''),
            manufacturersku=data.get('manufacturersku', '')
        )

    def to_dict(self) -> dict[str, str]:
        return {
            'id': str(self.id),
            'sku': self.sku,
            'style': self.style,
            'manufacturer': self.manufacturer,
            'name': self.name,
            'colour': self.colour,
            'size': self.size,
            'farbtyp': self.farbtyp,
            'goressentyp': self.goressentyp,
            'pcpack': str(self.pcpack),
            'pccarton': str(self.pccarton),
            'weightkg': self.weightkg,
            'status': self.status,
            'packshot': self.packshot,
            'ean': self.ean,
            'manufacturersku': self.manufacturersku
        }


@dataclass
class Artikel:
    id: int = field(default=0)  # Assuming id is an integer, and default is 0
    sku: str = field(default="")
    proizvajalcev_sku: str = field(default="")

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Artikel':
        return cls(
            id=int(data.get('id', 0)),  # Convert id to int
            sku=data.get('sku'),
            proizvajalcev_sku=data.get('proizvajalcev_sku')
        )

    @classmethod
    def to_dict(self) -> dict[str, str]:
        return {
            'sku': self.sku,
            'proizvajalcev_sku': self.proizvajalcev_sku
        }

@dataclass
class ArtikelDto:
    sku: str = field(default="")
    proizvalajcev_sku: str = field(default="")
    status: str = field(default="")    

@dataclass
class Barva:
    koda_barve: int = field(default=0)
    ime_barve: str = field(default="")
    sortirni_red_barve: int = field(default=0)


@dataclass
class Barvne_lastnosti: 
    koda_proizvajalca: str = field(default="")
    ime_barve: str = field(default="")
    cmyk: str = field(default="")

@dataclass
class Barvni_tip:
    sku: str = field(default="")
    tip_barve: str = field(default="")

@dataclass
class Cena:
    stil: str = field(default="")
    cena: float = field(default="")

@dataclass
class Drzava_izvora:
    stil: str = field(default="")
    izvor: str = field(default="")

@dataclass
class Ean:
    sku: str = field(default="")
    europska_stevilka_artikla: int = field(default=0)

@dataclass
class Firma:
    ime_proizvajalca: str = field(default="")
    koda_proizvajalca: int = field(default=0)

@dataclass
class Je_barve:
    sku: str = field(default="")
    barva: str = field(default="")

@dataclass
class Je_firme:
    sku: str = field(default="")
    koda_proizvajalca: int = field(default=0)

@dataclass
class Je_stila:
    sku: str = field(default="")
    stil: str = field(default="")

@dataclass
class Kolicina_v_kartonu:
    sku: str = field(default="")
    stevilo_v_kartonu: int = field(default=0)

@dataclass
class Kolicina_v_paketu:
    sku: str = field(default="")
    stevilo_v_paketu: int = field(default=0)

@dataclass
class Opis_anglescina:
    stil: str = field(default="")
    ime_anglescina: str = field(default="")
    opis_materiala_anglescina: str = field(default="")
    opis_artikla_anglescina: str = field(default="")

@dataclass
class Status:
    sku: str = field(default="")
    status: str = field(default="")

@dataclass
class Stil:
    stil: str = field(default="")
    ime_1: str = field(default="")

@dataclass
class Stran_kataloga:
    stil: str = field(default="")
    stran_kataloga: str = field(default="")

@dataclass
class Teza:
    sku: str = field(default="")
    teza: float = field(default=0)

@dataclass
class Velikost:
    sku: str = field(default="")
    velikost: str = field(default="")

@dataclass
class Velikostni_tip:
    sku: str = field(default="")
    tip_velikosti: str = field(default="")

@dataclass
class Vrsta_produkta:
    stil: str = field(default="")
    vrsta: str = field(default="")


@dataclass
class Uporabnik:
    username: str = field(default="")
    role: str = field(default="")
    password_hash: str = field(default="")
    last_login: str = field(default="")
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Uporabnik':
        return cls(
            username=data.get('username'),
            role=data.get('role'),
            password_hash=data.get('password_hash'),
            last_login=data.get('last_login')
        )
    @classmethod
    def to_dict(self) -> dict[str, str]:
        return {
            'username': self.username,
            'role': self.role,
            'password_hash': self.password_hash,
            'last_login': self.last_login
        }

@dataclass
class UporabnikDto:
    username: str = field(default="")
    role: str = field(default="")