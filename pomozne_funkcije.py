import re

def isci(pattern,string):
    if len(re.findall(pattern,string)) > 0:
        return True
    else:
        return False
    

def left_join(glavna,tabela,povezovalni_stolpec1,povezovalni_stolpec2):
    return f"Select * FROM {glavna} LEFT JOIN {tabela} ON {glavna}.{povezovalni_stolpec1}={tabela}.{povezovalni_stolpec2};"