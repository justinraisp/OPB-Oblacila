import bottle
from bottleext import get, post, run, request, template, redirect, static_file, url, response


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
    return bottle.template("artikli.html",filtri1=filtri1,filtri2=filtri2)

@bottle.route("/zaloga/")

def prikaz_strani_zaloga():
    return bottle.template("zaloga.html",filtri1=filtri1,filtri2=filtri2)

@bottle.route("/dodaj-zalogo/")

def prikaz_strani_zaloga():
    return bottle.template("dodaj-zalogo.html",filtri1=filtri1,filtri2=filtri2)

@bottle.route("/zaloga/izbrisi")

def izbrisi_zalogo():
    EAN = bottle.request.query.EAN
    return bottle.template("izbrisi.html",EAN=EAN)

@bottle.post("/zaloga/tocno-izbrisi")

def tocno_kaj_izbrisi_zalogo():
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
    return bottle.template("zaloga.html",filtri1=filtri1,filtri2=filtri2)


@bottle.post("/zaloga/dodaj")

def tocno_kaj_izbrisi_zalogo():
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
    return bottle.template("zaloga.html",filtri1=filtri1,filtri2=filtri2)

@bottle.post("/poizvedba/")

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
    # You can set 'napaka' to None if it's not needed in this context
    return template("registracija.html", napaka=None)

@post('/registracija')
def registracija_post():
    # Here you can handle the form submission and registration logic
    # For example, you can access form data like this:
    username = request.forms.get('username')
    role = request.forms.get('role')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')

    # Add your registration logic here and check for any errors
    auth.dodaj_uporabnika(username,role,password)
    # If registration is successful, you can redirect the user to the login page

    # For example:
    return template("prijava.html", napaka=None)
@post('/prijava')
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in njegovi roli.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("prijava.html", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)
        response.set_cookie("rola", prijava.role)
        
        # redirect v večino primerov izgleda ne deluje
        # redirect(url('index'))

        # Uporabimo kar template, kot v sami "index" funkciji
        return template('artikli.html', filtri1=filtri1, filtri2=filtri2)
        
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



if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)