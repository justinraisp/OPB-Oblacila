
library("readxl")
library("dplyr")
library(readr)

colour_templates <-read_excel("Artikli.xlsx", 
                       sheet = 6)

SKU_list<-read_csv2("Artikli.csv")
style_list<-read_excel("Artikli.xlsx", 
                       sheet = 3)
colour_codes<-read_excel("Artikli.xlsx", 
                       sheet = 4)
size_codes<-read_excel("Artikli.xlsx", 
                       sheet = 5)


artikel = SKU_list[c("SKU","ManufacturerSKU")]

je_stila = SKU_list[c("SKU","Style")]

barvni_tip  = SKU_list[c("SKU","Farbtyp")]

velikostni_tip = SKU_list[c("SKU","Groessentyp")]

je_barve = SKU_list[c("SKU","Colour")]

barva = colour_codes

barvne_lastnosti = colour_templates[c("Manuf-Code","ColourName","CMYK#01","RGB")]

la =  SKU_list[c("SKU","EAN")]
EAN = la[!is.na(la$EAN),]

firma = distinct(colour_templates[c(1,2)])

lala = SKU_list
colnames(lala)[3] = "Manuf-Name"
je_firme = left_join(lala, firma, by = "Manuf-Name")
je_firme = je_firme[c("SKU","Manuf-Code")]

kolicina_v_paketu = SKU_list[c("SKU","PC_Pack")]

kolicina_v_kartonu = SKU_list[c("SKU","PC_Carton")]

velikost = SKU_list[c("SKU","Size")]

status = SKU_list[c("SKU","Status")]

stil = style_list

teza = SKU_list[c("SKU","Weight_KG")]
