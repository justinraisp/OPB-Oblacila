from datetime import date
import datetime
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
        cena = izdelek.get('cena',1)
        if sku in trenutni_izdelki:
            trenutna_kolicina = trenutni_izdelki[sku].get('kolicina', 0)
            trenutna_cena = trenutni_izdelki[sku].get('cena',0)
            if kolicina == trenutna_kolicina:
                del trenutni_izdelki[sku]
            elif kolicina < trenutna_kolicina:
                trenutna_kolicina -= kolicina
                trenutni_izdelki[sku]['kolicina'] = trenutna_kolicina
                trenutna_cena -= cena
                trenutni_izdelki[sku]['cena'] = trenutna_cena
            else:
                pass
        
        self.izdelki = json.dumps(trenutni_izdelki)  

    def get_skupna_cena(self):
        skupna_cena = 0
        for nakup in self.izdelki.values():
            skupna_cena += nakup['cena']
        return skupna_cena         


@dataclass
class Transakcija:
    uporabnik: str = field(default="")
    datum: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    kosarica: str = field(default=json.dumps({}))
    skupna_cena: float = field(default=0)

    @classmethod
    def from_dict(cls, data: dict) -> 'Transakcija':
        return cls(
            uporabnik=data.get('uporabnik', ''),
            datum=data.get('datum', ''),
            kosarica=json.dumps(data.get('izdelki', {})),
            skupna_cena=float(data.get('skupna_cena', ''))
        )

    def to_dict(self) -> dict:
        return {
            'uporabnik': self.uporabnik,
            'datum': self.datum,
            'izdelki': json.loads(self.izdelki),
            'skupna_cena': self.skupna_cena,
        }

    def dodaj_nakup(self, kosarica: Kosarica):
        trenutna_kosarica = self.kosarica
        trenutna_kosarica.dodaj_izdelke(kosarica.izdelki)
        self.kosarica = trenutna_kosarica




@dataclass
class Glavna:
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
            sku=row[0],
            style=row[1],
            name=row[2],
            size=row[3],
            manufacturer=row[4],
            category=row[5],
            price=float(row[6]),
            name2=row[7],
            colour=row[8],
            status=row[9],
            material=row[10],
            description=row[11],
            origin=row[12]
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
class Zaloga: 
    sku: str = field(default="")
    kolicina: int = field(default=0)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Zaloga':
        return cls(
            sku=data.get('sku'),
            kolicina=int(data.get('kolicina', 0)) 
        )

    def to_dict(self) -> dict[str, str]:
        return {
            'sku': self.sku,
            'kolicina': self.kolicina
        }   
    
@dataclass
class OcenePredmetov: 
    sku: str = field(default="")
    ocena: float = field(default=0)
    st_ocen: int = field(default=0)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'OcenePredmetov':
        return cls(
            sku=data.get('sku'),
            ocena=float(data.get('ocena', 0)), 
            st_ocen=int(data.get('st_ocen', 0)), 
        )

    def to_dict(self) -> dict[str, str]:
        return {
            'sku': self.sku,
            'ocena': self.ocena,
            'st_ocen': self.st_ocen
        }

@dataclass
class Uporabnik_ocene:
    uporabnik: str = field(default="")
    ocene: str = field(default=json.dumps({}))

    @classmethod
    def from_dict(cls, data: dict) -> 'Uporabnik_ocene':
        return cls(
            uporabnik_id=data.get('uporabnik', ''),
            ocene=json.dumps(data.fet('ocene', {}))
        )

    def to_dict(self) -> dict:
        if self.ocene:
            return {
                'uporabnik': self.uporabnik,
                'ocene': json.loads(self.ocene)
            }
        else:
            return {
                'uporabnik': self.uporabnik,
                'ocene': {}
            }



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
class Stanje:
    uporabnik: str = field(default="")
    bilanca: float = field(default=0)
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Uporabnik':
        return cls(
            uporabnik=data.get('uporabnik'),
            bilanca=float(data.get('bilanca', 0))
        )
    @classmethod
    def to_dict(self) -> dict[str, str]:
        return {
            'uporabnik': self.uporabnik,
            'bilanca': str(self.bilanca)
        }



@dataclass
class Zgodovina:
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
        cena = izdelek.get('cena',1)
        if sku in trenutni_izdelki:
            trenutna_kolicina = trenutni_izdelki[sku].get('kolicina', 0)
            trenutna_cena = trenutni_izdelki[sku].get('cena',0)
            if kolicina == trenutna_kolicina:
                del trenutni_izdelki[sku]
            elif kolicina < trenutna_kolicina:
                trenutna_kolicina -= kolicina
                trenutni_izdelki[sku]['kolicina'] = trenutna_kolicina
                trenutna_cena -= cena
                trenutni_izdelki[sku]['cena'] = trenutna_cena
            else:
                pass
        
        self.izdelki = json.dumps(trenutni_izdelki)   


@dataclass
class UporabnikDto:
    username: str = field(default="")
    role: str = field(default="")