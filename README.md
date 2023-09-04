# OPB-Oblacila
V sklopu predmeta Osnove podatkovnih baz na Fakulteti za matematiko in fiziko, smo naredili projekt, ki predstavlja spletno trgovino za modne artikle.
Spletna trgovina obsega funkcionalnosti za dva tipa uporabnikov administratorja in gosta/kupca. Administratorji imajo možnost upravljanja z zalogo, vpogled v pretekle transakcije ter določeno statistiko. Kupci pa imajo moznost ogleda artiklov, nakup ter oceno le teh. Nakupi se izvedejo na podlagi naloženega denarja s strani kupca. 

## Uporaba
Ustvarimo okolje: 

`python3 -m venv env`

Aktiviramo okolje

 `source env/bin/activate`

Naložimo potrebne knjižnjice

 `env/bin/pip3 install -r requirenments.txt`
 
Naložimo si preostale datoteke in poženemo `main.py`. 

Potem pa se preko lokalnega url-ja registriramo glede na naše želje, se prijavimo in uporabljamo spletno trgovino.


### Spletni dostop
Lahko pa dostopamo do spletne aplikacije kar preko povezave:
* [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/justinraisp/OPB-Oblacila.git/HEAD?urlpath=proxy%2F8080)
