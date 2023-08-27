from math import ceil
import bottle
from bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user


from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps

import os

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)


repo = Repo()
auth = AuthService(repo)

filtri1 = ["SKU", "Proizvajalčev SKU","Stil","Tip barve","Tip velikosti","Barva","Koda barve","Ime barve", "Sortirni red barve","Koda proizvajalca","CMYK","RGB","Evropska številka artikla","Ime proizvajalca","Število v paketu","Število v kartonu","Velikost","Status","Teža","Ime","Ime (Nemščina)","Ime (Angleščina)","Ime (Češčina)","Opis materiala (Nemščina)","Opis materiala (Angleščina)","Opis materiala (Češčina)","Opis artikla (Angleščina)","Opis artikla (Nemščina)","Opis artikla (Češčina)","Stran kataloga","Cena","Izvor","Vrsta" ]
filtri2 = [ "SKU","proizvajalcev_SKU","stil","tip_barve","tip_velikosti","barva","koda_barve","ime_barve","sortirni_red_barve","koda_proizvajalca","CMYK","RGB","evropska_stevilka_artikla","ime_proizvajalca","stevilo_v_paketu","stevilo_v_kartonu","velikost","status","teza","ime","ime_nemscina","ime_anglescina","ime_cescina","opis_materiala_nemscina","opis_materiala_anglescina","opis_materiala_cescina","opis_artikla_anglescina","opis_artikla_nemscina","opis_artikla_cescina","stran_kataloga","cena","izvor","vrsta"]

filtri11 = [ "Proizvajalčev SKU","Tip barve","Tip velikosti","Koda barve", "Sortirni red barve","Koda proizvajalca","CMYK","RGB","Evropska številka artikla","Število v paketu","Število v kartonu","Teža","Ime (Nemščina)","Ime (Češčina)","Opis materiala (Nemščina)","Opis materiala (Češčina)","Opis artikla (Nemščina)","Opis artikla (Češčina)","Stran kataloga" ]
filtri22 = [ "proizvajalcev_SKU","tip_barve","tip_velikosti","koda_barve","sortirni_red_barve","koda_proizvajalca","CMYK","RGB","evropska_stevilka_artikla","stevilo_v_paketu","stevilo_v_kartonu","teza","ime","ime_nemscina","ime_cescina","opis_materiala_nemscina","opis_materiala_cescina","opis_artikla_nemscina","opis_artikla_cescina","stran_kataloga"]


def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        return template("prijava.html",uporabnik=None, rola=None, napaka="Potrebna je prijava!")        
    return decorated

@bottle.route("/")
@cookie_required
def prikaz_strani_artikel():
    uporabnik = request.get_cookie("uporabnik")
    rola= request.get_cookie("rola")

    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1))  #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    artikli = repo.dobi_gen(Glavna,take=artikli_na_stran,skip=zacetni_indeks)
    return template("artikli.html",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran)


@bottle.route("/artikel/<sku>")
@cookie_required
def prikaz_artikla(sku):
    uporabnik = request.get_cookie("uporabnik")
    rola = request.get_cookie("rola")

    artikel = repo.dobi_Artikel(sku)
    print(artikel)
    return template("artikel.html", artikel=artikel, rola=rola, uporabnik=uporabnik)


@bottle.route("/kosarica/")
@cookie_required
def prikaz_strani_kosarica():
    uporabnik = request.get_cookie("uporabnik")
    
    kosarica = repo.kosarica_nalozi(uporabnik)
    artikli = kosarica.to_dict()['izdelki']
    rola= request.get_cookie("rola")
    print(artikli)
    return template("kosarica.html",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,uporabnik=uporabnik)


@bottle.route("/dodaj_v_kosarico/<sku>", method="post")
@cookie_required
def dodaj_v_kosarico(sku):
    uporabnik = request.get_cookie("uporabnik")
    #artikel = repo.dobi_Artikel(sku)
    trenutna_kosarica = repo.kosarica_nalozi(uporabnik)
    kolicina = int(request.forms.get("kolicina_za_v_kosarico"))
    cena = float(request.forms.get("artikel_cena"))
    celotna_cena = cena * kolicina
    print(celotna_cena)
    izdelek = {
        "sku": sku,
        "kolicina": kolicina,
        "cena": celotna_cena
    }
    print(izdelek)
    trenutna_kosarica.dodaj_izdelek(izdelek)
    repo.kosarica_shrani(uporabnik,trenutna_kosarica.izdelki)

    bottle.redirect("/")


@bottle.route("/izbrisi_iz_kosarice/<sku>", method="post")
@cookie_required
def dodaj_v_kosarico(sku):
    uporabnik = request.get_cookie("uporabnik")
    #artikel = repo.dobi_Artikel(sku)
    trenutna_kosarica = repo.kosarica_nalozi(uporabnik)
    kolicina = int(request.forms.get("kolicina_izbrisi_kosarica"))
    izdelek = {
        "sku": sku,
        "kolicina": kolicina
    }
    print(izdelek)
    trenutna_kosarica.izbrisi(izdelek)
    repo.kosarica_shrani(uporabnik,trenutna_kosarica.izdelki)

    bottle.redirect("/kosarica/")    


@bottle.route("/zaloga/")
@cookie_required
def prikaz_strani_zaloga():
    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1))  #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    artikli = repo.dobi_gen(Glavna,take=artikli_na_stran,skip=zacetni_indeks)
    uporabnik = request.get_cookie("uporabnik")
    print(uporabnik)
    rola= request.get_cookie("rola")
    print(rola)
    print(max_stran)
    print(trenutna_stran)
    return template("zaloga.html",filtri1=filtri11,filtri2=filtri22,rola=rola,artikli=artikli,max_stran=max_stran,trenutna_stran=trenutna_stran)

@bottle.route("/dodaj-zalogo/")
@cookie_required
def prikaz_strani_zaloga():
    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1))  #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    artikli = repo.dobi_gen(Glavna,take=artikli_na_stran,skip=zacetni_indeks)
    uporabnik = request.get_cookie("uporabnik")
    print(uporabnik)
    rola= request.get_cookie("rola")
    
    print(rola)
    return template_user("dodaj-zalogo.html",filtri1=filtri11,filtri2=filtri22,artikli=artikli,max_stran=max_stran,trenutna_stran=trenutna_stran)

@bottle.route("/zaloga/izbrisi")
@cookie_required
def izbrisi_zalogo():
    EAN = bottle.request.query.EAN
    uporabnik = request.get_cookie("uporabnik")
    print(uporabnik)
    rola= request.get_cookie("rola")
    print(rola)
    return template("izbrisi.html",EAN=EAN,rola=rola)

@bottle.post("/zaloga/tocno-izbrisi")
@cookie_required
def tocno_kaj_izbrisi_zalogo():
    uporabnik = request.get_cookie("uporabnik")
    print(uporabnik)
    rola= request.get_cookie("rola")
    print(rola)
    EAN = bottle.request.query.EAN
    try:
        stevilo = int(bottle.request.forms["stevilo"]);
    except UnicodeError:
        stevilo = 0
    try:
        stevilo_kartonov = int(bottle.request.forms["stevilo_kartonov"]);
    except UnicodeError:
        stevilo_kartonov = 0
    try:
        stevilo_paketov = int(bottle.request.forms["stevilo_paketov"]);
    except UnicodeError:
        stevilo_paketov = 0
    #izbrisi iz zaloge
    return template("zaloga.html",filtri1=filtri11,filtri2=filtri22,rola=rola)


@bottle.post("/zaloga/dodaj")
@cookie_required
def tocno_kaj_izbrisi_zalogo():
    uporabnik = request.get_cookie("uporabnik")
    print(uporabnik)
    rola= request.get_cookie("rola")
    print(rola)
    try:
        EAN = int(bottle.request.forms["EAN"]);
    except UnicodeError:
        EAN = 0
    try:
        stevilo = int(bottle.request.forms["stevilo"]);
    except UnicodeError:
        stevilo = 0
    try:
        stevilo_kartonov = int(bottle.request.forms["stevilo_kartonov"]);
    except UnicodeError:
        stevilo_kartonov = 0
    try:
        stevilo_paketov = int(bottle.request.forms["stevilo_paketov"]);
    except UnicodeError:
        stevilo_paketov = 0
    #dodaj v zalogo
    return template("zaloga.html",filtri1=filtri11,filtri2=filtri22,rola=rola )

@bottle.post("/poizvedba/")
@cookie_required
def poizvedba():
    try:
        iskanje = bottle.request.forms["iskanje"];
    except UnicodeError:
        iskanje = False
    try:
        SKU = bottle.request.forms["SKU"]
        SKU = True
    except:
        SKU = False
    try:
        stil = bottle.request.forms["stil"]
        stil = True
    except:
        stil = False
    try:
        proizvajalcev_SKU = bottle.request.forms["proizvajalcev_SKU"]
        proizvajalcev_SKU = True
    except:
        proizvajalcev_SKU = False
    try:
        tip_barve = bottle.request.forms["tip_barve"]
        tip_barve = True
    except:
        tip_barve = False
    try:    
        tip_velikosti = bottle.request.forms["tip_velikosti"]
        tip_velikosti = True
    except:
        tip_velikosti = False
    try:
        barva = bottle.request.forms["barva"]
        barva = True
    except:
        barva = False
    try:    
        koda_barve = bottle.request.forms["koda_barve"]
        koda_barve = True
    except:
        koda_barve = False
    try:
        ime_barve = bottle.request.forms["ime_barve"]
        ime_barve=True
    except:
      ime_barve=False
    try:
        sortirni_red_barve = bottle.request.forms["sortirni_red_barve"]
        sortirni_red_barve = True
    except:
        sortirni_red_barve = False
    try:
        koda_proizvajalca = bottle.request.forms["koda_proizvajalca"]
        koda_proizvajalca = True
    except:
        koda_proizvajalca = False
    try:
        CMYK = bottle.request.forms["CMYK"]
        CMYK = True
    except:
        CMYK = False
    try:
        RGB = bottle.request.forms["RGB"]
        RGB = True
    except:
        RGB = False
    try:
        evropska_stevilka_artikla = bottle.request.forms["evropska_stevilka_artikla"]
        evropska_stevilka_artikla = True
    except:
        evropska_stevilka_artikla = False
    try:
        ime_proizvajalca = bottle.request.forms["ime_proizvajalca"]
        ime_proizvajalca = True
    except:
        ime_proizvajalca = False
    try:
        stevilo_v_paketu = bottle.request.forms["stevilo_v_paketu"]
        stevilo_v_paketu = True
    except:
        stevilo_v_paketu = False
    try:
        stevilo_v_kartonu = bottle.request.forms["stevilo_v_kartonu"]
        tevilo_v_kartonu = True
    except:
        stevilo_v_kartonu = False
    try:
        velikost = bottle.request.forms["velikost"]
        velikost = True
    except:
        velikost = False
    try:
        status = bottle.request.forms["status"]
        status = True
    except:
        status = False
    try:
        teza = bottle.request.forms["teza"]
        teza = True
    except:
        teza = False
    try:
        ime = bottle.request.forms["ime"]
        ime = True
    except:
        ime= False
    try:
        ime_nemscina = bottle.request.forms["ime_nemscina"]
        ime_nemscina = True
    except:
        ime_nemscina = False
    try:
        ime_anglescina = bottle.request.forms["ime_anglescina"]
        ime_anglescina = True
    except:
        ime_anglescina = False
    try:
        ime_cescina = bottle.request.forms["ime_cescina"]
        ime_cescina = True
    except:
        ime_cescina = False
    try:
        opis_materiala_nemscina = bottle.request.forms["opis_materiala_nemscina"]
        opis_materiala_nemscina = True
    except:
        opis_materiala_nemscina = False
    try:
        opis_materiala_anglescina = bottle.request.forms["opis_materiala_anglescina"]
        opis_materiala_anglescina = True
    except:
        opis_materiala_anglescina = False
    try:
        opis_materiala_cescina = bottle.request.forms["opis_materiala_cescina"]
        opis_materiala_cescina = True
    except:
        opis_materiala_cescina = False
    try:
        opis_artikla_anglescina= bottle.request.forms["opis_artikla_anglescina"]
        opis_artikla_anglescina = True
    except:
        opis_artikla_anglescina = False
    try:
        opis_artikla_nemscina = bottle.request.forms["opis_artikla_nemscina"]
        opis_artikla_nemscina = True
    except:
        opis_artikla_nemscina = False
    try:
        opis_artikla_cescina = bottle.request.forms["opis_artikla_cescina"]
        opis_artikla_cescina = True
    except:
        opis_artikla_cescina = False
    try:
        stran_kataloga = bottle.request.forms["stran_kataloga"]
        stran_kataloga = True
    except:
        stran_kataloga = False
    try:
        cena = bottle.request.forms["cena"]
        cena= True
    except:
        cena = False
    try:
        izvor = bottle.request.forms["izvor"]
        izvor = True
    except:
        izvor = False
    try:
        vrsta = bottle.request.forms["vrsta"]
        vrsta = True
    except:
        vrsta = False
    bottle.redirect("/")

@bottle.post("/poizvedba-zaloga/")
@cookie_required
def poizvedba_zaloga():
    try:
        iskanje = bottle.request.forms["iskanje"];
    except UnicodeError:
        iskanje = False
    try:
        SKU = bottle.request.forms["SKU"]
        SKU = True
    except:
        SKU = False
    try:
        stil = bottle.request.forms["stil"]
        stil = True
    except:
        stil = False
    try:
        proizvajalcev_SKU = bottle.request.forms["proizvajalcev_SKU"]
        proizvajalcev_SKU = True
    except:
        proizvajalcev_SKU = False
    try:
        tip_barve = bottle.request.forms["tip_barve"]
        tip_barve = True
    except:
        tip_barve = False
    try:    
        tip_velikosti = bottle.request.forms["tip_velikosti"]
        tip_velikosti = True
    except:
        tip_velikosti = False
    try:
        barva = bottle.request.forms["barva"]
        barva = True
    except:
        barva = False
    try:    
        koda_barve = bottle.request.forms["koda_barve"]
        koda_barve = True
    except:
        koda_barve = False
    try:
        ime_barve = bottle.request.forms["ime_barve"]
        ime_barve=True
    except:
      ime_barve=False
    try:
        sortirni_red_barve = bottle.request.forms["sortirni_red_barve"]
        sortirni_red_barve = True
    except:
        sortirni_red_barve = False
    try:
        koda_proizvajalca = bottle.request.forms["koda_proizvajalca"]
        koda_proizvajalca = True
    except:
        koda_proizvajalca = False
    try:
        CMYK = bottle.request.forms["CMYK"]
        CMYK = True
    except:
        CMYK = False
    try:
        RGB = bottle.request.forms["RGB"]
        RGB = True
    except:
        RGB = False
    try:
        evropska_stevilka_artikla = bottle.request.forms["evropska_stevilka_artikla"]
        evropska_stevilka_artikla = True
    except:
        evropska_stevilka_artikla = False
    try:
        ime_proizvajalca = bottle.request.forms["ime_proizvajalca"]
        ime_proizvajalca = True
    except:
        ime_proizvajalca = False
    try:
        stevilo_v_paketu = bottle.request.forms["stevilo_v_paketu"]
        stevilo_v_paketu = True
    except:
        stevilo_v_paketu = False
    try:
        stevilo_v_kartonu = bottle.request.forms["stevilo_v_kartonu"]
        tevilo_v_kartonu = True
    except:
        stevilo_v_kartonu = False
    try:
        velikost = bottle.request.forms["velikost"]
        velikost = True
    except:
        velikost = False
    try:
        status = bottle.request.forms["status"]
        status = True
    except:
        status = False
    try:
        teza = bottle.request.forms["teza"]
        teza = True
    except:
        teza = False
    try:
        ime = bottle.request.forms["ime"]
        ime = True
    except:
        ime= False
    try:
        ime_nemscina = bottle.request.forms["ime_nemscina"]
        ime_nemscina = True
    except:
        ime_nemscina = False
    try:
        ime_anglescina = bottle.request.forms["ime_anglescina"]
        ime_anglescina = True
    except:
        ime_anglescina = False
    try:
        ime_cescina = bottle.request.forms["ime_cescina"]
        ime_cescina = True
    except:
        ime_cescina = False
    try:
        opis_materiala_nemscina = bottle.request.forms["opis_materiala_nemscina"]
        opis_materiala_nemscina = True
    except:
        opis_materiala_nemscina = False
    try:
        opis_materiala_anglescina = bottle.request.forms["opis_materiala_anglescina"]
        opis_materiala_anglescina = True
    except:
        opis_materiala_anglescina = False
    try:
        opis_materiala_cescina = bottle.request.forms["opis_materiala_cescina"]
        opis_materiala_cescina = True
    except:
        opis_materiala_cescina = False
    try:
        opis_artikla_anglescina= bottle.request.forms["opis_artikla_anglescina"]
        opis_artikla_anglescina = True
    except:
        opis_artikla_anglescina = False
    try:
        opis_artikla_nemscina = bottle.request.forms["opis_artikla_nemscina"]
        opis_artikla_nemscina = True
    except:
        opis_artikla_nemscina = False
    try:
        opis_artikla_cescina = bottle.request.forms["opis_artikla_cescina"]
        opis_artikla_cescina = True
    except:
        opis_artikla_cescina = False
    try:
        stran_kataloga = bottle.request.forms["stran_kataloga"]
        stran_kataloga = True
    except:
        stran_kataloga = False
    try:
        cena = bottle.request.forms["cena"]
        cena= True
    except:
        cena = False
    try:
        izvor = bottle.request.forms["izvor"]
        izvor = True
    except:
        izvor = False
    try:
        vrsta = bottle.request.forms["vrsta"]
        vrsta = True
    except:
        vrsta = False
    bottle.redirect("/zaloga/")

@bottle.post("/poizvedba-dodaj/")
@cookie_required
def poizvedba_dodaj():
    try:
        iskanje = bottle.request.forms["iskanje"];
    except UnicodeError:
        iskanje = False
    try:
        SKU = bottle.request.forms["SKU"]
        SKU = True
    except:
        SKU = False
    try:
        stil = bottle.request.forms["stil"]
        stil = True
    except:
        stil = False
    try:
        proizvajalcev_SKU = bottle.request.forms["proizvajalcev_SKU"]
        proizvajalcev_SKU = True
    except:
        proizvajalcev_SKU = False
    try:
        tip_barve = bottle.request.forms["tip_barve"]
        tip_barve = True
    except:
        tip_barve = False
    try:    
        tip_velikosti = bottle.request.forms["tip_velikosti"]
        tip_velikosti = True
    except:
        tip_velikosti = False
    try:
        barva = bottle.request.forms["barva"]
        barva = True
    except:
        barva = False
    try:    
        koda_barve = bottle.request.forms["koda_barve"]
        koda_barve = True
    except:
        koda_barve = False
    try:
        ime_barve = bottle.request.forms["ime_barve"]
        ime_barve=True
    except:
      ime_barve=False
    try:
        sortirni_red_barve = bottle.request.forms["sortirni_red_barve"]
        sortirni_red_barve = True
    except:
        sortirni_red_barve = False
    try:
        koda_proizvajalca = bottle.request.forms["koda_proizvajalca"]
        koda_proizvajalca = True
    except:
        koda_proizvajalca = False
    try:
        CMYK = bottle.request.forms["CMYK"]
        CMYK = True
    except:
        CMYK = False
    try:
        RGB = bottle.request.forms["RGB"]
        RGB = True
    except:
        RGB = False
    try:
        evropska_stevilka_artikla = bottle.request.forms["evropska_stevilka_artikla"]
        evropska_stevilka_artikla = True
    except:
        evropska_stevilka_artikla = False
    try:
        ime_proizvajalca = bottle.request.forms["ime_proizvajalca"]
        ime_proizvajalca = True
    except:
        ime_proizvajalca = False
    try:
        stevilo_v_paketu = bottle.request.forms["stevilo_v_paketu"]
        stevilo_v_paketu = True
    except:
        stevilo_v_paketu = False
    try:
        stevilo_v_kartonu = bottle.request.forms["stevilo_v_kartonu"]
        tevilo_v_kartonu = True
    except:
        stevilo_v_kartonu = False
    try:
        velikost = bottle.request.forms["velikost"]
        velikost = True
    except:
        velikost = False
    try:
        status = bottle.request.forms["status"]
        status = True
    except:
        status = False
    try:
        teza = bottle.request.forms["teza"]
        teza = True
    except:
        teza = False
    try:
        ime = bottle.request.forms["ime"]
        ime = True
    except:
        ime= False
    try:
        ime_nemscina = bottle.request.forms["ime_nemscina"]
        ime_nemscina = True
    except:
        ime_nemscina = False
    try:
        ime_anglescina = bottle.request.forms["ime_anglescina"]
        ime_anglescina = True
    except:
        ime_anglescina = False
    try:
        ime_cescina = bottle.request.forms["ime_cescina"]
        ime_cescina = True
    except:
        ime_cescina = False
    try:
        opis_materiala_nemscina = bottle.request.forms["opis_materiala_nemscina"]
        opis_materiala_nemscina = True
    except:
        opis_materiala_nemscina = False
    try:
        opis_materiala_anglescina = bottle.request.forms["opis_materiala_anglescina"]
        opis_materiala_anglescina = True
    except:
        opis_materiala_anglescina = False
    try:
        opis_materiala_cescina = bottle.request.forms["opis_materiala_cescina"]
        opis_materiala_cescina = True
    except:
        opis_materiala_cescina = False
    try:
        opis_artikla_anglescina= bottle.request.forms["opis_artikla_anglescina"]
        opis_artikla_anglescina = True
    except:
        opis_artikla_anglescina = False
    try:
        opis_artikla_nemscina = bottle.request.forms["opis_artikla_nemscina"]
        opis_artikla_nemscina = True
    except:
        opis_artikla_nemscina = False
    try:
        opis_artikla_cescina = bottle.request.forms["opis_artikla_cescina"]
        opis_artikla_cescina = True
    except:
        opis_artikla_cescina = False
    try:
        stran_kataloga = bottle.request.forms["stran_kataloga"]
        stran_kataloga = True
    except:
        stran_kataloga = False
    try:
        cena = bottle.request.forms["cena"]
        cena= True
    except:
        cena = False
    try:
        izvor = bottle.request.forms["izvor"]
        izvor = True
    except:
        izvor = False
    try:
        vrsta = bottle.request.forms["vrsta"]
        vrsta = True
    except:
        vrsta = False
    bottle.redirect("/dodaj-zalogo/")


@get('/registracija')
def registracija():

    return template("registracija.html", napaka=None)

@post('/registracija')
def registracija_post():

    username = request.forms.get('username')
    rola = request.forms.get('role')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')
    if rola == "admin":
       return template("autorizacija.html", napaka=None, username=username, rola=rola, password=password)

    auth.dodaj_uporabnika(username,rola,password)

    if rola == "guest":
        nova_kosarica = Kosarica(uporabnik=username)
        repo.dodaj_gen(nova_kosarica)

    return template("prijava.html", napaka=None)


@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')
    try:
        if not auth.obstaja_uporabnik(username):
            return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")
    except Exception as e:
            return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")
    
    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)
        rola= prijava.role
        uporabnik = username
        
        # redirect v večino primerov izgleda ne deluje
        # redirect(url('index'))

        # Uporabimo kar template, kot v sami "index" funkciji
        artikli = repo.dobi_gen(Glavna)
        return template('artikli.html', filtri1=filtri11, filtri2=filtri22,artikli=artikli,rola=rola,trenutna_stran=1,max_stran=10)
        
    else:
        return template("prijava.html", uporabnik=None, rola=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")
   
@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    
    return template('prijava.html', uporabnik=None, rola=None, napaka=None)

@post("/autorizacija/")
def autorizacija():
    username = request.forms.get('username')
    auth_koda = request.forms.get('auth_koda')
    password = request.forms.get('password')

    if auth_koda == "FMF2023":
        auth.dodaj_uporabnika(username,"admin",password)
        return template("prijava.html", napaka=None)
    else : 
        return template("autorizacija.html", napaka="Napačna koda!", username=username, password=password)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)