import pandas as pd
from Data.Database import Repo

repo = Repo()


SKU_list = pd.read_excel("tabele/Artikli.xlsx", sheet_name=1)
Style_list = pd.read_excel("tabele/Artikli.xlsx", sheet_name=2)
Color_codes = pd.read_excel("tabele/Artikli.xlsx", sheet_name=3)
Size_codes = pd.read_excel("tabele/Artikli.xlsx", sheet_name=4)
Color_templates = pd.read_excel("tabele/Artikli.xlsx", sheet_name=5)





print(SKU_list)