# uvozimo psycopg2
import json
import random
import re
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

from typing import List, TypeVar, Type, Callable, Any
from Data.Modeli import *
from pandas import DataFrame
from re import sub
import Data.auth as auth
from datetime import date
#from dataclasses_json import dataclass_json
from dataclasses import fields
import dataclasses
# Ustvarimo generično TypeVar spremenljivko. Dovolimo le naše entitene, ki jih imamo tudi v bazi
# kot njene vrednosti. Ko dodamo novo entiteno, jo moramo dodati tudi v to spremenljivko.




T = TypeVar(
    "T",
    Glavna,
    Artikel,
    Uporabnik,
    UporabnikDto,
    Kosarica, 
    OcenePredmetov,
    Uporabnik_ocene,
    Transakcija
    )

import os

DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:

    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


    def dobi_gen(self, typ: Type[T], take=10, skip=0, sort_by=None, smer="DESC") -> List[T]:
        """Generična metoda, ki za podan vhodni dataclass vrne seznam teh objektov iz baze.
        Predpostavljamo, da je tabeli ime natanko tako kot je ime posameznemu dataclassu.
        """

        # ustvarimo sql select stavek, kjer je ime tabele typ.__name__ oz. ime razreda
        tbl_name = typ.__name__
        sql_cmd = f'''SELECT * FROM {tbl_name}'''
        if sort_by :
            sql_cmd += f' ORDER BY {sort_by} {smer}'

        sql_cmd += f' LIMIT {take} OFFSET {skip};'
        self.cur.execute(sql_cmd)

        columns = []
        for atribut in fields(typ):
            columns += [atribut.name]

        fetched_data = [dict(zip(columns, row)) for row in self.cur.fetchall()]

        return [typ.from_dict(data) for data in fetched_data]



    def dobi_gen_id(self, typ: Type[T], id: int | str, id_col = "id") -> T:
        """
        Generična metoda, ki vrne dataclass objekt pridobljen iz baze na podlagi njegovega idja.
        """
        tbl_name = typ.__name__
        sql_cmd = f'SELECT * FROM {tbl_name} WHERE {id_col} = %s';
        self.cur.execute(sql_cmd, (id,))

        d = self.cur.fetchone()

        if d is None:
            raise Exception(f'Vrstica z id-jem {id} ne obstaja v {tbl_name}');
    
        return typ.from_dict(d)
    
    def izbrisi_gen(self,  typ: Type[T], id: int | str, id_col = "id"):
        """
        Generična metoda, ki vrne dataclass objekt pridobljen iz baze na podlagi njegovega idja.
        """
        tbl_name = typ.__name__
        sql_cmd = f'Delete  FROM {tbl_name} WHERE {id_col} = %s';
        self.cur.execute(sql_cmd, (id,))
        self.conn.commit()


    
    def dodaj_gen(self, typ: T, serial_col="id", auto_commit=True):
        """
        Generična metoda, ki v bazo doda entiteto/objekt. V kolikor imamo definiram serial
        stolpec, objektu to vrednost tudi nastavimo.
        """

        tbl_name = type(typ).__name__

        cols =[c.name for c in dataclasses.fields(typ) if c.name != serial_col]
        
        sql_cmd = f'''
        INSERT INTO {tbl_name} ({", ".join(cols)})
        VALUES
        ({self.cur.mogrify(",".join(['%s']*len(cols)), [getattr(typ, c) for c in cols]).decode('utf-8')})
        '''

        if serial_col != None:
            sql_cmd += f'RETURNING {serial_col}'
        print(sql_cmd)
        self.cur.execute(sql_cmd)

        if serial_col != None:
            serial_val = self.cur.fetchone()[0]

            # Nastavimo vrednost serial stolpca
            setattr(typ, serial_col, serial_val)

        if auto_commit: self.conn.commit()

        # Dobro se je zavedati, da tukaj sam dataclass dejansko
        # "mutiramo" in ne ustvarimo nove reference. Return tukaj ni niti potreben.
      
    def dodaj_gen_list(self, typs: List[T], serial_col="id"):
        """
        Generična metoda, ki v bazo zapiše seznam objekton/entitet. Uporabi funkcijo
        dodaj_gen, le da ustvari samo en commit na koncu.
        """

        if len(typs) == 0: return # nič za narest

        # drugače dobimo tip iz prve vrstice
        typ = typs[0]

        tbl_name = type(typ).__name__

        cols =[c.name for c in dataclasses.fields(typ) if c.name != serial_col]
        sql_cmd = f'''
            INSERT INTO {tbl_name} ({", ".join(cols)})
            VALUES
            {','.join(
                self.cur.mogrify(f'({",".join(["%s"]*len(cols))})', i.to_dict()).decode('utf-8')
                for i in typs
                )}
        '''

        if serial_col != None:
            sql_cmd += f' RETURNING {serial_col};'

        self.cur.execute(sql_cmd)

        if serial_col != None:
            res = self.cur.fetchall()

            for i, d in enumerate(res):
                setattr(typs[i], serial_col, d[0])

        self.conn.commit()



    def posodobi_gen(self, typ: T, id_col = "id", auto_commit=True):
        """
        Generična metoda, ki posodobi objekt v bazi. Predpostavljamo, da je ime pripadajoče tabele
        enako imenu objekta, ter da so atributi objekta direktno vezani na ime stolpcev v tabeli.
        """

        tbl_name = type(typ).__name__
        
        id = getattr(typ, id_col)
        # dobimo vse atribute objekta razen id stolpca
        fields = [c.name for c in dataclasses.fields(typ) if c.name != id_col]

        sql_cmd = f'UPDATE {tbl_name} SET \n ' + \
                    ", \n".join([f'{field} = %s' for field in fields]) +\
                    f'WHERE {id_col} = %s'
        
        # iz objekta naredimo slovar (deluje samo za dataclasses_json)
        d = typ.to_dict()

        # sestavimo seznam parametrov, ki jih potem vsatvimo v sql ukaz
        parameters = [d[field] for field in fields]
        parameters.append(id)

        # izvedemo sql
        self.cur.execute(sql_cmd, parameters)
        if auto_commit: self.conn.commit()
        

    def posodobi_list_gen(self, typs : List[T], id_col = "id"):
        """
        Generična metoda, ki  posodobi seznam entitet(objektov). Uporabimo isti princip
        kot pri posodobi_gen funkciji, le da spremembe commitamo samo enkrat na koncu.
        """
        
        # Posodobimo vsak element seznama, pri čemer sprememb ne comitamo takoj na bazi
        for typ in typs:
            self.posodobi_gen(typ, id_col=id_col, auto_commit=False)

        # Na koncu commitamo vse skupaj
        self.conn.commit()


    def camel_case(self, s):
        """
        Pomožna funkcija, ki podan niz spremeni v camel case zapis.
        """
        
        s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
        return ''.join(s)     

    def col_to_sql(self, col: str, col_type: str, use_camel_case=True, is_key=False):
        """
        Funkcija ustvari del sql stavka za create table na podlagi njegovega imena
        in (python) tipa. Dodatno ga lahko opremimo še z primary key omejitvijo
        ali s serial lastnostjo. Z dodatnimi parametri, bi lahko dodali še dodatne lastnosti.
        """

        # ali stolpce pretvorimo v camel case zapis?
        if use_camel_case:
            col = self.camel_case(col)
        
        match col_type:

            case "int":
                return f'"{col}" BIGINT{" PRIMARY KEY" if  is_key else ""}'
            case "int32":
                return f'"{col}" BIGINT{" PRIMARY KEY" if  is_key else ""}'
         
            case "int64":
                return f'"{col}" BIGINT{" PRIMARY KEY" if  is_key else ""}'
            case "float":
                return f'"{col}" FLOAT'
            case "float32":
                return f'"{col}" FLOAT'
            case "float64":
                return f'"{col}" FLOAT'
        
        # če ni ujemanj stolpec naredimo kar kot text
        return f'"{col}" TEXT{" PRIMARY KEY" if  is_key else ""}'
    
    def df_to_sql_create(self, df: DataFrame, name: str, add_serial=False, use_camel_case=True) -> str:
        """
        Funkcija ustvari in izvede sql stavek za create table na podlagi podanega pandas DataFrame-a. 
        df: DataFrame za katerega zgradimo sql stavek
        name: ime nastale tabele v bazi
        add_serial: opcijski parameter, ki nam pove ali želimo dodat serial primary key stolpec
        """

        # dobimo slovar stolpcev in njihovih tipov
        cols = dict(df.dtypes)
        print(cols)
        cols_sql = ""

        # dodamo serial primary key
        if add_serial: cols_sql += 'Id SERIAL PRIMARY KEY,\n'
        
        # dodamo ostale stolpce
        # tukaj bi stolpce lahko še dodatno filtrirali, preimenovali, itd.
        cols_sql += ",\n".join([self.col_to_sql(col, str(typ), use_camel_case=use_camel_case) for col, typ in cols.items()])


        # zgradimo končen sql stavek
        sql = f'''CREATE TABLE IF NOT EXISTS {name}(
            {cols_sql}
        )'''


        self.cur.execute(sql)
        self.conn.commit()
        

    def df_to_sql_insert(self, df:DataFrame, name:str, use_camel_case=True):
        """
        Vnese DataFrame v postgresql bazo. Paziti je treba pri velikosti dataframa,
        saj je sql stavek omejen glede na dolžino. Če je dataframe prevelik, ga je potrebno naložit
        po delih (recimo po 100 vrstic naenkrat), ali pa uporabit bulk_insert.
        df: DataFrame, ki ga želimo prenesti v bazo
        name: Ime tabele kamor želimo shranit podatke
        use_camel_case: ali pretovrimo stolpce v camel case zapis
        """

        cols = list(df.columns)

        # po potrebi pretvorimo imena stolpcev
        if use_camel_case: cols = [self.camel_case(c) for c in cols]

        # ustvarimo sql stavek, ki vnese več vrstic naenkrat
        sql_cmd = f'''INSERT INTO {name} ({", ".join([f'"{c}"' for c in cols])})
            VALUES 
            {','.join(
                self.cur.mogrify(f'({",".join(["%s"]*len(cols))})', i).decode('utf-8')
                for i in df.itertuples(index=False)
                )}
        '''

        # izvedemo ukaz
        self.cur.execute(sql_cmd)
        self.conn.commit()

    def dobi_Artikel(self, sku):
        # Preverimo, če Artikel že obstaja
        print(sku)
        self.cur.execute("""SELECT * FROM glavna WHERE sku = %s;""",(sku,))
        row = self.cur.fetchone()
        if row:
            return(Glavna.create_glavna_from_row(row))
        
        raise Exception("Artikel z imenom " + sku + " ne obstaja")
    
    def dobi_Artikle(self, sku_list):
        skus = tuple(sku_list) 
        placeholders = ",".join(["%s"] * len(sku_list)) 
        query = f"""SELECT * FROM glavna WHERE sku IN ({placeholders});"""
        
        self.cur.execute(query, skus)
        rows = self.cur.fetchall()
        artikli = []

        for row in rows:
            artikli.append(Glavna.create_glavna_from_row(row))

        return artikli



    def dodaj_Artikel(self, Artikel: Artikel) -> Artikel:

        # Preverimo, če Artikel že obstaja
        self.cur.execute("""
            SELECT id, ime, kategorija from Artikel
            WHERE ime = %s;
          """, (Artikel.ime,))
        
        row = self.cur.fetchone()
        if row:
            Artikel.id = row[0]
            return Artikel

        # Sedaj dodamo Artikel
        self.cur.execute("""
            INSERT INTO Artikel (ime, kategorija)
              VALUES (%s, %s) RETURNING id; """, (Artikel.ime, Artikel.kategorija))
        Artikel.id = self.cur.fetchone()[0]
        self.conn.commit()
        return Artikel
    
    def artikli(self) -> List[int]:
        artikli = self.cur.execute(
             """
            SELECT i.id FROM artikel i

            """)

        return [id for id in artikli]
    
    def ustvari_tabelo_glavna(self):
        sql = """
        CREATE TABLE IF NOT EXISTS glavna (
            sku TEXT PRIMARY KEY,
            style TEXT,
            name TEXT,
            size TEXT,
            manufacturer TEXT,
            category TEXT,
            price FLOAT,
            name2 TEXT, 
            colour TEXT,
            status TEXT, 
            material TEXT, 
            description TEXT,
            origin TEXT
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        print("Tabela 'glavna' ustvarjena ali že obstaja.")

    def ustvari_tabelo_kosarica(self):
        sql = """
        CREATE TABLE IF NOT EXISTS kosarica (
            Uporabnik TEXT PRIMARY KEY,
            Izdelki JSONB
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        print("Tabela 'kosarica' ustvarjena ali že obstaja.")

    def ustvari_tabelo_ocene(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ocene_predmetov (
            sku TEXT PRIMARY KEY,
            ocena FLOAT,
            st_ocen INT
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        print("Tabela 'ocena' ustvarjena ali že obstaja.")

    def ustvari_tabelo_transakcija(self):
        sql = """
        CREATE TABLE IF NOT EXISTS transakcija (
            uporabnik TEXT,
            datum TEXT,
            kosarica JSONB,
            skupna_cena FLOAT
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        print("Tabela 'transakcija' ustvarjena ali že obstaja.")


    def ustvari_tabelo_stanje(self):
        sql = """
        CREATE TABLE IF NOT EXISTS stanje (
            uporabnik TEXT PRIMARY KEY,
            bilanca FLOAT
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        print("Tabela 'ocena' ustvarjena ali že obstaja.")

    def ustvari_tabelo_uporabnik_ocene(self):
        sql = """
        CREATE TABLE IF NOT EXISTS uporabnik_ocene (
            uporabnik TEXT PRIMARY KEY,
            ocene JSONB
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        print("Tabela 'ocena' ustvarjena ali že obstaja.")    

    def ustvari_tabelo_zaloga(self):
        sql = """
        CREATE TABLE IF NOT EXISTS zaloga (
            sku TEXT PRIMARY KEY,
            kolicina INT
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        print("Tabela 'zaloga' ustvarjena ali že obstaja.")     

    def join_tables(self, tabela1, tabela2, join_column):

        sql = f"""
        SELECT *
        FROM {tabela1}
        LEFT JOIN {tabela2} ON {tabela1}.{join_column} = {tabela2}.{join_column};
        """
        self.cur.execute(sql)
        result = self.cur.fetchall()
        print(result[0:3])
        return result

    def pridobi_ocene(self, artikli, max=False):
        skuji = [artikel.sku for artikel in artikli]
        ocene = []
        if max: 
            self.cur.execute("")
        for sku in skuji:
            self.cur.execute("""SELECT sku, ocena, st_ocen FROM ocenepredmetov WHERE sku = %s;""", (sku,))
            result = self.cur.fetchone()
            if result:
                sku, ocena, st_ocen = result
                ocene.append(OcenePredmetov(sku,ocena,st_ocen))
        
        return ocene

    def glavna_nalozi_iskanje(self, iskalni_niz, stolpec):
        pattern = f"%{iskalni_niz}%"
        if stolpec == "price":
            pattern = f"{iskalni_niz}%"
            self.cur.execute(f"""SELECT * FROM glavna WHERE CAST(price AS TEXT) ILIKE %s;""", (pattern,))
        else:
            self.cur.execute(f"""SELECT * FROM glavna WHERE {stolpec} ILIKE %s;""", (pattern,))
        rows = self.cur.fetchall()
        columns = []
        for atribut in fields(Glavna):
            columns += [atribut.name]
        artikli = [dict(zip(columns, row)) for row in rows]
        return [Glavna.from_dict(artikel) for artikel in artikli]

    def zaloga_nalozi_iskanje(self, iskalni_niz):
        pattern = f"%{iskalni_niz}%"
        self.cur.execute("""SELECT * FROM zaloga WHERE Sku ILIKE %s;""", (pattern,))
        rows = self.cur.fetchall()
        columns = []
        for atribut in fields(Zaloga):
            columns += [atribut.name]
        artikli = [dict(zip(columns, row)) for row in rows]
        return [Zaloga.from_dict(artikel) for artikel in artikli]        

    def transakcija_shrani(self, transakcija):
        uporabnik = transakcija.uporabnik
        datum = transakcija.datum
        kosarica = transakcija.kosarica
        
        skupna_cena = transakcija.skupna_cena
        self.cur.execute("INSERT INTO transakcija (uporabnik, datum, kosarica, skupna_cena) VALUES (%s, %s, %s, %s);",
                            (uporabnik, datum, json.dumps(kosarica), skupna_cena))

        self.conn.commit()

    def transakcija_nalozi(self, uporabnik):
        self.cur.execute("SELECT datum, kosarica, skupna_cena FROM transakcija WHERE uporabnik = %s;", (uporabnik,))
        row = self.cur.fetchone()
        if row:
            datum = row[0]
            kosarica = row[1]
            skupna_cena = row[2]
            return Transakcija(uporabnik, datum, kosarica, skupna_cena)
        else:
            return None
        
    def pridobi_zgodovino_nakupov(self, uporabnik,rola):
        if rola == "guest":
            self.cur.execute("SELECT datum, kosarica, skupna_cena FROM transakcija WHERE uporabnik = %s;", (uporabnik,))
            rows = self.cur.fetchall()
            zgodovina = []
            for row in rows:
                datum = row[0]
                kosarica = row[1]
                skupna_cena = row[2]
                zgodovina.append({"datum": datum, "kosarica": kosarica, "skupna_cena": skupna_cena})
        else:     
            self.cur.execute("SELECT * FROM transakcija;")
            rows = self.cur.fetchall()
            zgodovina = []
            for row in rows:
                uporabnik = row[0]
                datum = row[1]
                kosarica = row[2]
                skupna_cena = row[3]
                zgodovina.append({"uporabnik": uporabnik, "datum": datum, "kosarica": kosarica, "skupna_cena": skupna_cena})
                print(zgodovina)
        return zgodovina

    def oceni_artikel(self, sku, nova_ocena):
        self.cur.execute("SELECT * FROM ocenepredmetov WHERE  sku = %s;", (sku,))
        trenutna_ocena = self.cur.fetchone()
        if trenutna_ocena:
            st_ocen = int(trenutna_ocena['st_ocen']) + 1
            nova_povprecna_ocena = float((trenutna_ocena['ocena'] * trenutna_ocena['st_ocen'] + nova_ocena) / st_ocen)
            self.cur.execute("UPDATE ocenepredmetov SET ocena = %s, st_ocen = %s WHERE  sku = %s;",
                            (nova_povprecna_ocena, st_ocen, sku,))
        else:
            self.cur.execute("INSERT INTO ocenepredmetov (sku, ocena, st_ocen) VALUES (%s, %s, 1);",
                            (sku, nova_ocena,))
        self.conn.commit()

    def pridobi_zgodovino_ocen(self, uporabnik):
        self.cur.execute("SELECT ocene FROM uporabnik_ocene WHERE uporabnik = %s;", (uporabnik,))
        ocene_uporabnika = self.cur.fetchone()
        if ocene_uporabnika:
            return ocene_uporabnika[0]
        else: return None

    def oceni_artikel_uporabnik(self, uporabnik, sku, nova_ocena):
        ocene = self.pridobi_zgodovino_ocen(uporabnik)
        self.oceni_artikel(sku, nova_ocena)
        ocene[sku] = nova_ocena
        ocene_json = json.dumps(ocene)
        self.cur.execute("UPDATE uporabnik_ocene SET ocene = %s WHERE uporabnik = %s;", (ocene_json, uporabnik))
              
        self.conn.commit()


    def kosarica_shrani(self,uporabnik,izdelki):
        self.cur.execute("SELECT * FROM kosarica WHERE uporabnik = %s;", (uporabnik,))
        trenutna = self.cur.fetchone()
        #print(trenutna)
        if trenutna:
            self.cur.execute("UPDATE kosarica SET izdelki = %s WHERE uporabnik = %s;", (json.dumps(izdelki), uporabnik))
        else:
            self.cur.execute("INSERT INTO kosarica (uporabnik, izdelki) VALUES (%s, %s);", (uporabnik, json.dumps(izdelki)))

        self.conn.commit()
        
    def kosarica_nalozi(self, uporabnik):
        self.cur.execute("SELECT izdelki FROM kosarica WHERE uporabnik = %s;", (uporabnik,))
        row = self.cur.fetchone()
        if row:
            kosarica_data = row[0]
            return Kosarica(uporabnik,kosarica_data)
        else:
            return None
           
    def dobi_stanje(self, uporabnik):
        self.cur.execute("SELECT bilanca FROM stanje WHERE uporabnik = %s;", (uporabnik,))
        row = self.cur.fetchone()
        if row:
            return Stanje(uporabnik,row[0])
        else: 
            return None
        
    def posodobi_zaloga(self, sku, kolicina_sprememba,dodaj=True):
        self.cur.execute("SELECT kolicina FROM zaloga WHERE sku = %s;", (sku,))
        row = self.cur.fetchone()
        if row:
            kolicina = row[0]
            if dodaj:
                kolicina += kolicina_sprememba
            else: 
                kolicina -= kolicina_sprememba
            self.cur.execute("UPDATE zaloga SET kolicina = %s WHERE sku = %s;", (kolicina,sku,))
        else:
            self.cur.execute("INSERT INTO zaloga (sku, kolicina) VALUES (%s, %s);", (sku, kolicina_sprememba,))
            self.cur.execute("INSERT INTO ocenepredmetov (sku, ocena, st_ocen) VALUES (%s,%s,%s);", (sku,0,0,))
        self.conn.commit()        

    def posodobi_stanje(self,uporabnik, vsota):
        stanje = self.dobi_stanje(uporabnik=uporabnik)
        bilanca = stanje.bilanca
        bilanca += vsota
        bilanca = round(bilanca,2)
        self.cur.execute("UPDATE stanje SET bilanca = %s WHERE uporabnik = %s;", (bilanca,uporabnik))
        self.conn.commit()

    def transakcija_statistika(self, mesec):
        self.cur.execute("SELECT COUNT(*) FROM transakcija")
        stevilo_transakcij = self.cur.fetchone()[0]

        self.cur.execute("SELECT COUNT(*) FROM transakcija WHERE SUBSTRING(datum, 6, 2) = %s;", (mesec,))
        stevilo_transakcij_v_mesecu = self.cur.fetchone()[0]

        self.cur.execute("SELECT SUM(skupna_cena) FROM transakcija WHERE SUBSTRING(datum, 6, 2) = %s;", (mesec,))
        skupen_znesek_narocil_v_mesecu = self.cur.fetchone()[0] 

        self.cur.execute("SELECT SUM(skupna_cena) FROM transakcija;")
        skupen_znesek = self.cur.fetchone()[0]

        self.conn.commit()
        return stevilo_transakcij, stevilo_transakcij_v_mesecu, skupen_znesek, skupen_znesek_narocil_v_mesecu
    
    def izdelek_statistika(self, mesec):
        self.cur.execute("""
            SELECT
                key AS izdelek,
                SUM((value->>'kolicina')::numeric) AS skupna_kolicina
            FROM
                transakcija,
                jsonb_each(transakcija.kosarica)
            GROUP BY
                key
            ORDER BY
                skupna_kolicina DESC
            LIMIT 1;
        """)

        najbolj_prodajan = self.cur.fetchone()[0]

        self.cur.execute("""
            SELECT
                key AS izdelek,
                SUM((value->>'kolicina')::numeric) AS skupna_kolicina
            FROM
                transakcija,
                jsonb_each(transakcija.kosarica)
            WHERE SUBSTRING(datum, 6, 2) = %s
            GROUP BY
                key
            ORDER BY
                skupna_kolicina DESC
            LIMIT 1;
        """, (mesec,))

        najbolj_prodajan_v_mesecu = self.cur.fetchone()[0]
        self.conn.commit()    
        return najbolj_prodajan,najbolj_prodajan_v_mesecu
    
    def uporabnik_statistika(self,mesec ):
        self.cur.execute("""
            SELECT
                uporabnik,
                SUM(skupna_cena) AS skupna_vsota
            FROM
                transakcija
            GROUP BY
                uporabnik
            ORDER BY
                skupna_vsota DESC
            LIMIT 1;
        """)

        najvisja_vsota = self.cur.fetchone()
        
        self.cur.execute("""
            SELECT
                uporabnik,
                SUM(skupna_cena) AS skupna_vsota
            FROM
                transakcija
            WHERE SUBSTRING(datum, 6, 2) = %s
            GROUP BY
                uporabnik
            ORDER BY
                skupna_vsota DESC
            LIMIT 1;
        """,(mesec,))
        najvisja_vsota_mesec = self.cur.fetchone()

        if najvisja_vsota:
            uporabnik = najvisja_vsota[0]
            uporabnik_mesec = najvisja_vsota_mesec[0]
            return uporabnik,  uporabnik_mesec
        else:
            return None
        
    def count_glavna(self, stolpec="*"):
        self.cur.execute("SELECT COUNT(%s) FROM glavna;", (stolpec,))
        stevilo = self.cur.fetchone()[0]
        return stevilo
            
    def generiraj_nakljucne_ocene(self, st_ocen):
        self.cur.execute("""SELECT sku FROM glavna;""")
        artikli = self.cur.fetchall()
        self.cur.execute("DELETE FROM ocene_predmetov;")
        for artikel in artikli:
            ocena = 0
            st = random.randint(st_ocen //2, st_ocen)
            for i in range(st):
                nakljucna_ocena = random.randint(2,5)
                ocena += nakljucna_ocena
            ocena = ocena / st
            self.cur.execute("INSERT INTO ocene_predmetov (sku, ocena, st_ocen) VALUES (%s,%s,%s);", (artikel[0], ocena, st))
        self.conn.commit()

    def generiraj_nakljucno_zalogo(self, max_kolicina):
        self.cur.execute("""SELECT sku FROM glavna;""")
        artikli = self.cur.fetchall()
        for artikel in artikli:
            kolicina = random.randint(max_kolicina //2, max_kolicina)
            self.cur.execute("INSERT INTO zaloga (sku, kolicina) VALUES (%s,%s);", (artikel[0], kolicina))
        self.conn.commit()
