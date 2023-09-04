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
    #repo.df_to_sql_create(df, ime, add_serial=False, use_camel_case=True)
    repo.ustvari_tabelo_glavna()

    # uvozimo podatke v to isto tabelo
    repo.df_to_sql_insert(df, ime, use_camel_case=False)

#repo.ustvari_tabelo_kosarica()
#repo.ustvari_tabelo_ocene()
#repo.ustvari_tabelo_stanje()
#repo.ustvari_tabelo_uporabnik_ocene()
#repo.ustvari_tabelo_transakcije()
#repo.generiraj_nakljucne_ocene(20)
#repo.ustvari_tabelo_zaloga()
#repo.generiraj_nakljucno_zalogo(730)

#uvozi_csv(r"tabele/glavna.txt", "Glavna")

