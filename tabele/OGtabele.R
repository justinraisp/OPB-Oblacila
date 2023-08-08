library("readxl")
library("dplyr")
library(readr)
library("gt")
library("tidyverse")


colour_templates <-read_excel("Artikli.xlsx", 
                              sheet = 6)

SKU_list<-read_csv2("Artikli.csv")
style_list<-read_excel("Artikli.xlsx", 
                       sheet = 3)
colour_codes<-read_excel("Artikli.xlsx", 
                         sheet = 4)
size_codes<-read_excel("Artikli.xlsx", 
                       sheet = 5)

glavna = left_join(SKU_list, style_list, by='Style') 

glavna = glavna |>
  gt() |>
  fmt_currency(
    columns = "Orientation Price",
    currency = "EUR")


glavna = as.data.frame(glavna)



glavna[[28]] = str_replace(glavna[[28]], "&#8364;", "€")

glavna =  dplyr::select(glavna,c(1,2,3,4,5,12,16,20,21,22,28,30,32))
glavna = glavna[c(1,2,4,3,13,11,8,5,6,9,10,12)]
colnames(glavna) = c("SKU", "Style", "Name", "Manufacturer", "Category", "Price", "Name2", "Colour", "Status", "Material", "Description", "Origin")

write.csv(glavna,"C:\\Users\\justin\\Desktop\\glavna.txt" , row.names=FALSE, sep=";",encoding="UTF-8")

artikel_ = SKU_list[c("SKU","ManufacturerSKU")]
colnames(artikel_)[1] = "sku"
colnames(artikel_)[2] = "proizvajalcev_sku"

je_stila_ = SKU_list[c("SKU","Style")]
colnames(je_stila_)[1] = "sku"
colnames(je_stila_)[2] = "stil"

barvni_tip_  = SKU_list[c("SKU","Farbtyp")]
colnames(barvni_tip_)[1] = "sku"
colnames(barvni_tip_)[2] = "tip_barve"

velikostni_tip_ = SKU_list[c("SKU","Groessentyp")]
colnames(velikostni_tip_)[1] = "sku"
colnames(velikostni_tip_)[2] = "tip_velikosti"

je_barve_ = SKU_list[c("SKU","Colour")]
colnames(je_barve_)[1] = "sku"
colnames(je_barve_)[2] = "barva"

barva_ = colour_codes
colnames(barva_)[1] = "koda_barve"
colnames(barva_)[2] = "ime_barve"
colnames(barva_)[3] = "sortirni_red_barve"

barvne_lastnosti_ = colour_templates[c("Manuf-Code","ColourName","CMYK#01","RGB")]
colnames(barvne_lastnosti_)[1] = "koda_proizvajalca"
colnames(barvne_lastnosti_)[2] = "ime_barve"
colnames(barvne_lastnosti_)[3] = "cmyk"
colnames(barvne_lastnosti_)[4] = "rgb"

la =  SKU_list[c("SKU","EAN")]
ean_ = la[!is.na(la$EAN),]
colnames(ean_)[1] = "sku"
colnames(ean_)[2] = "europska_stevilka_artikla"

firma_ = distinct(colour_templates[c(1,2)])
colnames(firma_)[1] = "ime_proizvajalca"
colnames(firma_)[2] = "koda_proizvajalca"

lala = SKU_list
colnames(lala)[3] = "ime_proizvajalca"
je_firme = left_join(lala, firma_, by = "ime_proizvajalca")
je_firme_ = je_firme[c("SKU","koda_proizvajalca")]
je_firme_ = je_firme_[!is.na(je_firme_$koda_proizvajalca),]
colnames(je_firme_)[1] = "sku"
colnames(je_firme_)[2] = "koda_proizvajalca"

kolicina_v_paketu_ = SKU_list[c("SKU","PC_Pack")]
colnames(kolicina_v_paketu_)[1] = "sku"
colnames(kolicina_v_paketu_)[2] = "stevilo_v_paketu"

kolicina_v_kartonu_ = SKU_list[c("SKU","PC_Carton")]
colnames(kolicina_v_kartonu_)[1] = "sku"
colnames(kolicina_v_kartonu_)[2] = "stevilo_v_kartonu"

velikost_ = SKU_list[c("SKU","Size")]
colnames(velikost_)[1] = "sku"
colnames(velikost_)[2] = "velikost"

status_ = SKU_list[c("SKU","Status")]
colnames(status_)[1] = "sku"
colnames(status_)[2] = "status"

stil = style_list

teza_ = SKU_list[c("SKU","Weight_KG")]
colnames(teza_)[1] = "sku"
colnames(teza_)[2] = "teza"

stil_ = stil[c("Style","Name1")]
colnames(stil_)[1] = "stil"
colnames(stil_)[2] = "ime_1"

opis_nemscina_ = stil[c("Style","Name2 (german)", "Material-Description (german)", "Product-Description (german)")]
colnames(opis_nemscina_)[1] = "stil"
colnames(opis_nemscina_)[2] = "ime_nemscina"
colnames(opis_nemscina_)[3] = "opis_materiala_nemscina"
colnames(opis_nemscina_)[4] = "opis_artikla_nemscina"


opis_anglescina_ = stil[c("Style","Name2 (english)", "Material-Description (english)", "Product-Description (english)")]
colnames(opis_anglescina_)[1] = "stil"
colnames(opis_anglescina_)[2] = "ime_anglescina"
colnames(opis_anglescina_)[3] = "opis_materiala_anglescina"
colnames(opis_anglescina_)[4] = "opis_artikla_anglescina"

opis_cescina_ = stil[c("Style","Name2 (czech)", "Material-Description (czech)", "Product-Description (czech)")]
colnames(opis_cescina_)[1] = "stil"
colnames(opis_cescina_)[2] = "ime_cescina"
colnames(opis_cescina_)[3] = "opis_materiala_cescina"
colnames(opis_cescina_)[4] = "opis_artikla_cescina"


stran_katalog_ = stil[c("Style", "Catalouge Page")]
colnames(stran_katalog_)[1] = "stil"
colnames(stran_katalog_)[2] = "stran_kataloga"

cena_ = stil[c("Style", "Orientation Price")]
colnames(cena_)[1] = "stil"
colnames(cena_)[2] = "cena"

drzava_izvora_ =  stil[c("Style", "Origin")]
colnames(drzava_izvora_)[1] = "stil"
colnames(drzava_izvora_)[2] = "izvor"

vrsta_produkta_ =  stil[c("Style", "Categories")]
colnames(vrsta_produkta_)[1] = "stil"
colnames(vrsta_produkta_)[2] = "vrsta"

# write.csv(vrsta_produkta_ ,"C:\\Users\\matic\\Desktop\\tabele\\vrsta_produkta.txt" , row.names=FALSE)
# write.csv(je_stila_ ,"C:\\Users\\matic\\Desktop\\tabele\\je_stila.txt" , row.names=FALSE)
# write.csv(kolicina_v_kartonu_ ,"C:\\Users\\matic\\Desktop\\tabele\\kolicina_v_kartonu.txt" , row.names=FALSE)
# write.csv(kolicina_v_paketu_ ,"C:\\Users\\matic\\Desktop\\tabele\\kolicina_v_paketu.txt" , row.names=FALSE)
# write.csv(opis_anglescina_ ,"C:\\Users\\matic\\Desktop\\tabele\\opis_anglescina.txt" , row.names=FALSE)
# write.csv(opis_cescina_ ,"C:\\Users\\matic\\Desktop\\tabele\\opis_cescina.txt" , row.names=FALSE)
# write.csv(opis_nemscina_ ,"C:\\Users\\matic\\Desktop\\tabele\\opis_nemscina.txt" , row.names=FALSE)
# write.csv(status_ ,"C:\\Users\\matic\\Desktop\\tabele\\status.txt" , row.names=FALSE)
# write.csv(stil_ ,"C:\\Users\\matic\\Desktop\\tabele\\stil.txt" , row.names=FALSE)
# write.csv(stran_katalog_ ,"C:\\Users\\matic\\Desktop\\tabele\\stran_kataloga.txt" , row.names=FALSE)
# write.csv(teza_ ,"C:\\Users\\matic\\Desktop\\tabele\\teza.txt" , row.names=FALSE)
# write.csv(velikost_ ,"C:\\Users\\matic\\Desktop\\tabele\\velikost.txt" , row.names=FALSE)
# write.csv(velikostni_tip_ ,"C:\\Users\\matic\\Desktop\\tabele\\velikostni_tip.txt" , row.names=FALSE)
# write.csv(artikel_ ,"C:\\Users\\matic\\Desktop\\tabele\\artikel.txt" , row.names=FALSE)
# write.csv(barva_ ,"C:\\Users\\matic\\Desktop\\tabele\\barva.txt" , row.names=FALSE)
# write.csv(barvne_lastnosti_ ,"C:\\Users\\matic\\Desktop\\tabele\\barvne_lastnosti.txt" , row.names=FALSE)
# write.csv(barvni_tip_ ,"C:\\Users\\matic\\Desktop\\tabele\\barvni_tip.txt" , row.names=FALSE)
# write.csv(cena_ ,"C:\\Users\\matic\\Desktop\\tabele\\cena.txt" , row.names=FALSE)
# write.csv(drzava_izvora_ ,"C:\\Users\\matic\\Desktop\\tabele\\drzava_izvora.txt" , row.names=FALSE)
# write.csv(ean_ ,"C:\\Users\\matic\\Desktop\\tabele\\ean.txt" , row.names=FALSE)
# write.csv(firma_ ,"C:\\Users\\matic\\Desktop\\tabele\\firma.txt" , row.names=FALSE)
# write.csv(je_barve_ ,"C:\\Users\\matic\\Desktop\\tabele\\je_barve.txt" , row.names=FALSE)
# write.csv(je_firme_ ,"C:\\Users\\matic\\Desktop\\tabele\\je_firme.txt" , row.names=FALSE)
