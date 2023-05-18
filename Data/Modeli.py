from dataclasses import dataclass, field

@dataclass
class Artikel:
    sku: str = field(default="")
    proizvalajcev_sku: str = field(default="")

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