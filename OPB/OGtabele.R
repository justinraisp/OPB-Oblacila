
library("readxl")

colour_templates <-read_excel("Artikli.xlsx", 
                       sheet = 6)

SKU_list<-read_excel("Artikli.xlsx", 
                       sheet = 2)
style_list<-read_excel("Artikli.xlsx", 
                       sheet = 3)
colour_codes<-read_excel("Artikli.xlsx", 
                       sheet = 4)
size_codes<-read_excel("Artikli.xlsx", 
                       sheet = 5)