import pandas as pd
from pandas import DataFrame
from Modeli import *
from Database import Repo

repo = Repo()



def uvozi_csv(pot, ime):
    """
    Uvozimo csv v bazo brez večjih posegov v podatke.
    Ustvarimo pandasov DataFrame ter nato z generično metodo ustvarimo ter
    napolnimo tabelo v postgresql bazi.
    """
    df = pd.read_csv(pot, sep=",", encoding="Windows-1250",  quotechar='"')

    # Zamenjamo pomišljaje z prazno vrednostjo
    df.replace(to_replace="-", value="", inplace=True)

    # Naredimo tabelo z dodatnim serial primary key stolpcem
    repo.df_to_sql_create(df, ime, add_serial=True, use_camel_case=True)

    # uvozimo podatke v to isto tabelo
    repo.df_to_sql_insert(df, ime, use_camel_case=True)

#repo.ustvari_tabelo_kosarica()


#uvozi_csv("tabele/artikel.txt", "Artikel")
#uvozi_csv("tabele/barva.txt", "Barva")
#uvozi_csv("tabele/barvne_lastnosti.txt", "Barvne_lastnosti")
#uvozi_csv("tabele/barvni_tip.txt", "Barvni_tip")
#uvozi_csv("tabele/cena.txt", "Cena")
#uvozi_csv("tabele/drzava_izvora.txt", "Drzava_izvora")
#uvozi_csv("tabele/ean.txt", "Ean")
#uvozi_csv("tabele/firma.txt", "Firma")
#uvozi_csv("tabele/je_barve.txt", "Je_barve")
#uvozi_csv("tabele/je_firme.txt", "Je_firme")
#uvozi_csv("tabele/je_stila.txt", "Je_stila")
#uvozi_csv("tabele/kolicina_v_kartonu.txt", "Kolicina_v_kartonu")
#uvozi_csv("tabele/kolicina_v_paketu.txt", "Kolicina_v_paketu")
#uvozi_csv("tabele/opis_anglescina.txt", "Opis_anglescina")
#uvozi_csv("tabele/status.txt", "Status")
#uvozi_csv("tabele/stil.txt", "Stil")
#uvozi_csv("tabele/stran_kataloga.txt", "Stran_kataloga")
#uvozi_csv("tabele/teza.txt", "Teza")
#uvozi_csv("tabele/velikost.txt", "Velikost")
#uvozi_csv("tabele/velikostni_tip.txt", "Velikostni_tip")
#uvozi_csv("tabele/vrsta_produkta.txt", "Vrsta_produkta")
#uvozi_csv("Artikli.csv", "Artikli")
#uvozi_csv(r"tabele/glavna.txt", "Glavna")
