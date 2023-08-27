import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass
class Kosarica:
    uporabnik: str = field(default="")
    izdelki: str = field(default=json.dumps({}))

    @classmethod
    def from_dict(cls, data: dict) -> 'Kosarica':
        return cls(
            uporabnik=data.get('uporabnik', ''),
            izdelki=json.dumps(data.get('izdelki', {}))
        )

    def to_dict(self) -> dict:
        if self.izdelki:
            return {
                'uporabnik': self.uporabnik,
                'izdelki': json.loads(self.izdelki)
            }
        else:
            return {
                'uporabnik': self.uporabnik,
                'izdelki': {}
            }

    def dodaj_izdelek(self, izdelek: dict):
        # Preverimo, ali je izdelek že v košarici
        trenutni_izdelki = json.loads(self.izdelki) if self.izdelki else {}
        sku = izdelek.get('sku')
        kolicina = izdelek.get('kolicina', 1)
        cena = izdelek.get('cena',0)
        cena_izdelka = cena / kolicina
        if sku in trenutni_izdelki:
            trenutni_kolicina = trenutni_izdelki[sku].get('kolicina', 0)
            trenutni_kolicina += kolicina
            trenutni_izdelki[sku]['kolicina'] = trenutni_kolicina
            trenutni_cena = trenutni_kolicina * cena_izdelka
            trenutni_izdelki[sku]['cena'] = trenutni_cena

        else:
            trenutni_izdelki[sku] = {'kolicina': kolicina, 'cena': cena}
        
        self.izdelki = json.dumps(trenutni_izdelki)

    def izbrisi(self, izdelek: dict):
    # Preverimo, ali je izdelek v košarici
        trenutni_izdelki = json.loads(self.izdelki) if self.izdelki else {}
        sku = izdelek.get('sku')
        kolicina = izdelek.get('kolicina',1)
        if sku in trenutni_izdelki:
            trenutna_kolicina = trenutni_izdelki[sku].get('kolicina', 0)
            if kolicina == trenutna_kolicina:
                del trenutni_izdelki[sku]
            elif kolicina < trenutna_kolicina:
                trenutna_kolicina -= kolicina
                trenutni_izdelki[sku]['kolicina'] = trenutna_kolicina
            else:
                pass
        
        self.izdelki = json.dumps(trenutni_izdelki)        

@dataclass
class Glavna:
    id: int = field(default=0)
    sku: str = field(default="")
    style: str = field(default="")
    name: str = field(default="")
    size: str = field(default="")
    manufacturer: str = field(default="")
    category: str = field(default="")
    price: str = field(default="")
    name2: str = field(default="")
    colour: str = field(default="")
    status: str = field(default="")
    material: str = field(default="")
    description: str = field(default="")
    origin: str = field(default="")

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Glavna':
        return cls(
            id=int(data.get('id', 0)),
            sku=data.get('sku', ''),
            style=data.get('style', ''),
            name=data.get('name', ''),
            size=data.get('size',''),
            manufacturer=data.get('manufacturer', ''),
            category=data.get("category", ""),
            price=data.get("price", ""),
            name2=data.get("name2",""),
            colour=data.get('colour', ''),
            status=data.get('status', ''),
            material=data.get('material', ''),
            description=data.get('description', ''),
            origin=data.get('origin', ''),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            'sku': self.sku,
            'style': self.style,
            'name': self.name,
            'size': self.size,
            'manufacturer': self.manufacturer,
            'category': self.category,
            'price': self.price,
            'name2': self.name2,
            'colour': self.colour,
            'status': self.status,
            'material': self.material,
            'description': self.description,
            'origin': self.origin
        }
    def create_glavna_from_row(row):
        return Glavna(
            id=row[0],
            sku=row[1],
            style=row[2],
            name=row[3],
            size=row[4],
            manufacturer=row[5],
            category=row[6],
            price=float(row[7]),
            name2=row[8],
            colour=row[9],
            status=row[10],
            material=row[11],
            description=row[12],
            origin=row[13]
        )


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