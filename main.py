#!/usr/bin/python
# -*- encoding: utf-8 -*-

from dataclasses import fields
from math import ceil
import bottle
from bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import psycopg2
from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps
import Data.auth
import os

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get("POSTGRES_PORT",5432)


repo = Repo()
auth = AuthService(repo)

filtri1 = ["SKU", "Proizvajalčev SKU","Stil","Tip barve","Tip velikosti","Barva","Koda barve","Ime barve", "Sortirni red barve","Koda proizvajalca","CMYK","RGB","Evropska številka artikla","Ime proizvajalca","Število v paketu","Število v kartonu","Velikost","Status","Teža","Ime","Ime (Nemščina)","Ime (Angleščina)","Ime (Češčina)","Opis materiala (Nemščina)","Opis materiala (Angleščina)","Opis materiala (Češčina)","Opis artikla (Angleščina)","Opis artikla (Nemščina)","Opis artikla (Češčina)","Stran kataloga","Cena","Izvor","Vrsta" ]
filtri2 = [ "SKU","proizvajalcev_SKU","stil","tip_barve","tip_velikosti","barva","koda_barve","ime_barve","sortirni_red_barve","koda_proizvajalca","CMYK","RGB","evropska_stevilka_artikla","ime_proizvajalca","stevilo_v_paketu","stevilo_v_kartonu","velikost","status","teza","ime","ime_nemscina","ime_anglescina","ime_cescina","opis_materiala_nemscina","opis_materiala_anglescina","opis_materiala_cescina","opis_artikla_anglescina","opis_artikla_nemscina","opis_artikla_cescina","stran_kataloga","cena","izvor","vrsta"]

filtri11 = [ "Proizvajalčev SKU","Tip barve","Tip velikosti","Koda barve", "Sortirni red barve","Koda proizvajalca","CMYK","RGB","Evropska številka artikla","Število v paketu","Število v kartonu","Teža","Ime (Nemščina)","Ime (Češčina)","Opis materiala (Nemščina)","Opis materiala (Češčina)","Opis artikla (Nemščina)","Opis artikla (Češčina)","Stran kataloga" ]
filtri22 = [ "proizvajalcev_SKU","tip_barve","tip_velikosti","koda_barve","sortirni_red_barve","koda_proizvajalca","CMYK","RGB","evropska_stevilka_artikla","stevilo_v_paketu","stevilo_v_kartonu","teza","ime","ime_nemscina","ime_cescina","opis_materiala_nemscina","opis_materiala_cescina","opis_artikla_nemscina","opis_artikla_cescina","stran_kataloga"]

glavna_stolpci = ["sku", 
    "style", 
    "name", 
    "size", 
    "manufacturer", 
    "category", 
    "price", 
    "name2", 
    "colour", 
    "status", 
    "material", 
    "description", 
    "origin"]

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
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1))
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    #print(repo.dobi_statistiko())
    if rola == "guest":
        artikli = repo.dobi_gen(Glavna,take=artikli_na_stran,skip=zacetni_indeks)
        ocene = repo.pridobi_ocene(artikli)
        return template("artikli_guest.html",sortiranje="",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran, stanje=stanje, uporabnik=uporabnik, poizvedba= "", ocene=ocene,glavna_stolpci=glavna_stolpci)
    if rola == "admin":
        artikli = repo.dobi_gen(Zaloga,take=artikli_na_stran,skip=zacetni_indeks)
        return template("artikli_admin.html",sortiranje="",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran, stanje=stanje, uporabnik=uporabnik, poizvedba="")


@bottle.route("/glavna/")
@cookie_required
def glavna():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1))  #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    #print(repo.dobi_statistiko())
    if rola == "guest":
        artikli = repo.dobi_gen(Glavna,take=artikli_na_stran,skip=zacetni_indeks)
        ocene = repo.pridobi_ocene(artikli)
        return template("artikli_guest.html",sortiranje="",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran, stanje=stanje, uporabnik=uporabnik, poizvedba= "", ocene=ocene,glavna_stolpci=glavna_stolpci)
    if rola == "admin":
        artikli = repo.dobi_gen(Zaloga,take=artikli_na_stran,skip=zacetni_indeks)
        return template("artikli_admin.html",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran, stanje=stanje, uporabnik=uporabnik, poizvedba="")



@bottle.route("/razvrsti/", method=["POST", "GET"])
def razvrsti():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    if request.forms.get("sortiranje"):
        sortiranje = request.forms.get("sortiranje")
        stolpec = request.forms.get("sortiranje").split()[0]
        smer = request.forms.get("sortiranje").split()[1]
        response.set_cookie("sortiranje", request.forms.get("sortiranje"))
    else:
        stolpec = request.get_cookie("sortiranje").split()[0]
        smer = request.get_cookie("sortiranje").split()[1]
    trenutna_stran = int(request.query.get("stran", 1))
    artikli_na_stran = 10
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    if stolpec == "price":
        artikli = repo.dobi_gen(Glavna,take=artikli_na_stran,skip=zacetni_indeks,sort_by=stolpec, smer=smer)
        ocene = repo.pridobi_ocene(artikli)
    else:
        ocene = repo.dobi_gen(OcenePredmetov,take=artikli_na_stran,skip=zacetni_indeks,sort_by=stolpec, smer=smer)
        skuji = [ocena.sku for ocena in ocene]
        artikli = repo.dobi_Artikle(skuji)
    max_stran = ceil(106871 / artikli_na_stran)
    return template("artikli_guest.html",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran, stanje=stanje, uporabnik=uporabnik, poizvedba="razvrsti", ocene=ocene,glavna_stolpci=glavna_stolpci,stolpec=stolpec,smer=smer,sortiranje="")

@bottle.route("/artikel/<sku>")
@cookie_required
def artikel(sku):
    uporabnik = request.get_cookie("uporabnik")
    rola = request.get_cookie("rola")
    artikel = repo.dobi_Artikel(sku)
    stanje= repo.dobi_stanje(uporabnik)
    return template("artikel.html", artikel=artikel, rola=rola, uporabnik=uporabnik, stanje=stanje)


@bottle.route("/kosarica/")
@cookie_required
def kosarica():
    uporabnik = request.get_cookie("uporabnik")
    kosarica = repo.kosarica_nalozi(uporabnik)
    artikli = kosarica.to_dict()['izdelki']
    rola= request.get_cookie("rola")
    stanje= repo.dobi_stanje(uporabnik)
    return template("kosarica.html",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,uporabnik=uporabnik, stanje=stanje, napaka=None)

@bottle.route("/uporabnik_guest/")
@cookie_required
def uporabnik_guest():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    return template("uporabnik_guest.html", stanje=stanje, uporabnik=uporabnik, rola= rola)

@bottle.route("/statistika/")
@cookie_required
def statistika():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    trenutni_mesec = date.today().strftime('%m')
    stevilo_vseh_narocil, stevilo_narocil_v_mesecu, skupen_znesek_narocil, skupen_znesek_narocil_v_mesecu = repo.transakcija_statistika(trenutni_mesec)
    najbolj_prodajan_izdelek, najbolj_prodajan_izdelek_v_mesecu = repo.izdelek_statistika(trenutni_mesec)
    najboljsi_uporabnik, najboljsi_uporabnik_mesec = repo.uporabnik_statistika(trenutni_mesec)
  
    return template("statistika.html", stanje=stanje, uporabnik=uporabnik,rola=rola,
                    stevilo_vseh_narocil=stevilo_vseh_narocil,stevilo_narocil_v_mesecu=stevilo_narocil_v_mesecu,
                    skupen_znesek_narocil=skupen_znesek_narocil, skupen_znesek_narocil_v_mesecu=skupen_znesek_narocil_v_mesecu,
                    najbolj_prodajan_izdelek=najbolj_prodajan_izdelek,najbolj_prodajan_izdelek_v_mesecu=najbolj_prodajan_izdelek_v_mesecu,
                    najboljsi_uporabnik=najboljsi_uporabnik,najboljsi_uporabnik_mesec=najboljsi_uporabnik_mesec)

@bottle.route("/uporabnik_admin/")
@cookie_required
def uporabnik_admin():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje("admin")
    rola= request.get_cookie("rola")
    return template("uporabnik_admin.html",rola=rola , stanje=stanje, uporabnik=uporabnik)

@bottle.route("/zgodovina")
@cookie_required
def zgodovina():
    uporabnik = request.get_cookie("uporabnik")
    ocene_predmetov = repo.pridobi_zgodovino_ocen(uporabnik)
    rola= request.get_cookie("rola")
    stanje= repo.dobi_stanje(uporabnik)
    zgodovina = repo.pridobi_zgodovino_nakupov(uporabnik,rola)
    return template("zgodovina.html", uporabnik=uporabnik, zgodovina=zgodovina, ocene_predmetov=ocene_predmetov,rola=rola,stanje=stanje)


@bottle.route("/dodaj_denar", method="post")
@cookie_required
def dodaj_denar():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    vsota = float(request.forms.get("vsota"))
    credit_card = request.forms.get("credit-card")
    repo.posodobi_stanje(uporabnik, vsota)
    bottle.redirect(url("uporabnik_guest"))


@bottle.route("/dodaj_v_kosarico/<sku>", method="post")
@cookie_required
def dodaj_v_kosarico(sku):
    uporabnik = request.get_cookie("uporabnik")
    trenutna_kosarica = repo.kosarica_nalozi(uporabnik)
    kolicina = int(request.forms.get("kolicina_za_v_kosarico"))
    cena = float(request.forms.get("artikel_cena"))
    celotna_cena = cena * kolicina
    izdelek = {
        "sku": sku,
        "kolicina": kolicina,
        "cena": celotna_cena
    }
    trenutna_kosarica.dodaj_izdelek(izdelek)
    repo.kosarica_shrani(uporabnik,trenutna_kosarica.izdelki)

    bottle.redirect(url("glavna"))


@bottle.route("/izbrisi_iz_kosarice/<sku>", method="post")
@cookie_required
def izbrisi_iz_kosarice(sku):
    uporabnik = request.get_cookie("uporabnik")
    #artikel = repo.dobi_Artikel(sku)
    trenutna_kosarica = repo.kosarica_nalozi(uporabnik)
    if request.forms.get("kolicina_izbrisi_kosarica"):
        kolicina = int(request.forms.get("kolicina_izbrisi_kosarica"))
    else: kolicina = trenutna_kosarica.to_dict()['izdelki'][sku]['kolicina']
    cena = trenutna_kosarica.to_dict()['izdelki'][sku]['cena']  / trenutna_kosarica.to_dict()['izdelki'][sku]['kolicina']
    celotna_cena = cena * kolicina
    izdelek = {
        "sku": sku,
        "kolicina": kolicina,
        "cena": celotna_cena
    }
    trenutna_kosarica.izbrisi(izdelek)
    repo.kosarica_shrani(uporabnik,trenutna_kosarica.izdelki)

    bottle.redirect(url("kosarica"))    

@bottle.route("/izvedi_nakup", method="post")
@cookie_required
def izvedi_nakup():
    uporabnik = request.get_cookie("uporabnik")
    trenutno_stanje = repo.dobi_stanje(uporabnik)
    skupna_cena = 0
    kosarica = repo.kosarica_nalozi(uporabnik)
    izdelki_v_kosarici = kosarica.to_dict().get("izdelki", {})  
    for izdelek in izdelki_v_kosarici.values():
        skupna_cena += izdelek["cena"]
    if trenutno_stanje.bilanca < skupna_cena:
        return template("kosarica.html", artikli=izdelki_v_kosarici, uporabnik=uporabnik, stanje=trenutno_stanje,
                        napaka="Nimate dovolj sredstev za nakup.")  
    for izdelek in izdelki_v_kosarici.keys():
        repo.posodobi_zaloga(izdelek, izdelki_v_kosarici[izdelek]["kolicina"],dodaj=False)
    repo.posodobi_stanje(uporabnik, -skupna_cena)
    datum = date.today().isoformat()
    repo.transakcija_shrani(Transakcija(uporabnik=uporabnik, datum=datum,kosarica=izdelki_v_kosarici,skupna_cena=skupna_cena))
    repo.kosarica_shrani(uporabnik, {})
    bottle.redirect(url("kosarica"))


@bottle.route("/oceni_artikel/<sku>", method="post")
@cookie_required
def oceni_artikel(sku):
    ocena = int(request.forms.get('ocena'))
    uporabnik = request.get_cookie("uporabnik")
    repo.oceni_artikel_uporabnik(uporabnik,sku,ocena)
    rola= request.get_cookie("rola")
    bottle.redirect(url("zgodovina"))


@bottle.route("/zaloga/")
@cookie_required
def zaloga():
    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1)) #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    artikli = repo.dobi_gen(Glavna,take=artikli_na_stran,skip=zacetni_indeks)
    uporabnik = request.get_cookie("uporabnik")
    rola= request.get_cookie("rola")
    return template("zaloga.html",filtri1=filtri11,filtri2=filtri22,rola=rola,artikli=artikli,max_stran=max_stran,trenutna_stran=trenutna_stran, uporabnik=uporabnik)


@bottle.route("/dodaj_zalogo/<sku>", method="post")
@cookie_required
def dodaj_zalogo(sku):
    kolicina_dodaj = int(request.forms.get("kolicina"))
    repo.posodobi_zaloga(sku, kolicina_dodaj)
    bottle.redirect(url("glavna"))


@bottle.route("/dodaj_zalogo_stran/")
@cookie_required
def dodaj_zalogo_stran():
    uporabnik = request.get_cookie("uporabnik")
    rola= request.get_cookie("rola")
    artikel = Glavna()
    artikli = repo.dobi_gen(Glavna)
   
    return template_user("dodaj-zalogo.html",filtri1=filtri11,filtri2=filtri22,artikel = artikel,artikli=artikli)

@bottle.route("/dodaj_zalogo_novo/", method="post")
@cookie_required
def dodaj_zalogo_novo():
    podatki = {}
    for atribut in fields(Glavna()):
        podatki[atribut.name] = request.forms.get(atribut.name)
    artikel = Glavna(**podatki)
    kolicina = int(request.forms.get("kolicina"))
    repo.posodobi_zaloga(podatki["sku"], kolicina)
   
    repo.dodaj_gen(artikel,serial_col=None)
    #repo.posodobi_zaloga(sku, kolicina_dodaj,dodaj=True)
    bottle.redirect(url("glavna"))

@bottle.route("/zaloga/izbrisi")
@cookie_required
def izbrisi_zalogo():
    EAN = bottle.request.query.EAN
    uporabnik = request.get_cookie("uporabnik")
    rola= request.get_cookie("rola")
    return template("izbrisi.html",EAN=EAN,rola=rola)

@bottle.route("/poizvedba_prikazi/<iskanje>/<po_cem_iscemo>/")
@cookie_required
def poizvedba_prikazi(iskanje, po_cem_iscemo):
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    rezultati_iskanja = repo.glavna_nalozi_iskanje(iskanje,stolpec= po_cem_iscemo)
    artikli_na_stran = 10
    max_stran = ceil(len(rezultati_iskanja) / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1))  #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    artikli = rezultati_iskanja[zacetni_indeks:koncni_indeks]
    poizvedba = "poizvedba_prikazi/" + iskanje + "/" +  po_cem_iscemo
    ocene = repo.pridobi_ocene(artikli)
    
    return template("artikli_guest.html",sortiranje="",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran, stanje=stanje, uporabnik=uporabnik, poizvedba=poizvedba, ocene=ocene,glavna_stolpci=glavna_stolpci,iskanje=iskanje, po_cem_iscemo= po_cem_iscemo)

@bottle.post("/poizvedba/")
@cookie_required
def poizvedba():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran =  int(request.query.get("stran", 1)) #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    po_cem_iscemo = request.forms.get("iskanje_po_cem_iscemo")
    try:
        iskanje = bottle.request.forms["iskanje"]
    except UnicodeError:
        iskanje = False
        rezultati_iskanja = None

    bottle.redirect(url("poizvedba_prikazi",iskanje=iskanje, po_cem_iscemo= po_cem_iscemo))


@bottle.route("/poizvedba_zaloga_prikazi/<iskanje>")
@cookie_required
def poizvedba_zaloga_prikazi(iskanje):
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    rezultati_iskanja = repo.zaloga_nalozi_iskanje(iskanje)
    artikli_na_stran = 10
    max_stran = ceil(len(rezultati_iskanja) / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1)) #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    artikli = rezultati_iskanja[zacetni_indeks:koncni_indeks]
    poizvedba = "poizvedba_zaloga_prikazi/" + iskanje
    return template("artikli_admin.html",filtri1=filtri11,filtri2=filtri22, artikli=artikli,rola=rola,trenutna_stran=trenutna_stran, max_stran=max_stran, stanje=stanje, uporabnik=uporabnik, poizvedba=poizvedba,iskanje=iskanje)


@bottle.post("/poizvedba_zaloga/")
@cookie_required
def poizvedba_zaloga():
    uporabnik = request.get_cookie("uporabnik")
    stanje = repo.dobi_stanje(uporabnik)
    rola= request.get_cookie("rola")
    artikli_na_stran = 10
    max_stran = ceil(106871 / artikli_na_stran)
    trenutna_stran = int(request.query.get("stran", 1))  #Default stran je prva
    zacetni_indeks = (trenutna_stran - 1) * artikli_na_stran
    koncni_indeks = zacetni_indeks + artikli_na_stran
    try:
        iskanje = bottle.request.forms["iskanje"]
    except UnicodeError:
        iskanje = False

    bottle.redirect(url("poizvedba_zaloga_prikazi",iskanje=iskanje))

@bottle.post("/poizvedba-dodaj/")
@cookie_required
def poizvedba_dodaj():
    try:
        iskanje = bottle.request.forms["iskanje"];
    except UnicodeError:
        iskanje = False

    bottle.redirect(url("dodaj_zalogo"))


@get('/registracija')
def registracija():
    return template("registracija.html", napaka=None)

@post('/registracija')
def registracija_post():

    username = request.forms.get('username')
    rola = request.forms.get('role')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')
    if password==confirm_password:
        try:
            if auth.obstaja_uporabnik(username):
                return template("registracija.html", napaka="Uporabnik s tem imenom že obstaja")
        except Exception as e:
                if rola == "guest":
                    auth.dodaj_uporabnika(username,rola,password)
                    nova_kosarica = Kosarica(uporabnik=username)
                    repo.dodaj_gen(nova_kosarica)
                    novo_stanje = Stanje(uporabnik=username)
                    repo.dodaj_gen(novo_stanje,serial_col=None)
                    nove_ocene = Uporabnik_ocene(uporabnik=username)
                    repo.dodaj_gen(nove_ocene,serial_col=None)

                if rola == "admin":
                    return template("autorizacija.html", napaka=None, username=username, rola=rola, password=password)

                return template("prijava.html", napaka=None)
    else:
        return template("registracija.html", napaka="Gesli se ne ujemata")


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
        # Uporabimo kar template, kot v sami "index" funkciji
        artikli = repo.dobi_gen(Glavna)
        stanje = repo.dobi_stanje(uporabnik)
        
        if not stanje: 
            stanje= Stanje(uporabnik=username)
            repo.dodaj_gen(stanje,serial_col=None)
        #return template(f'artikli_{rola}.html', filtri1=filtri11, filtri2=filtri22,artikli=artikli,rola=rola,trenutna_stran=1,max_stran=10, stanje=stanje, uporabnik=uporabnik)
        redirect(url("glavna"))
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
    
@get("/print/")
def print():
    printek = request.forms.get('print')
    
conn = psycopg2.connect(database=Data.auth.db, host=Data.auth.host,
                        user=Data.auth.user, password=Data.auth.password, port=DB_PORT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)