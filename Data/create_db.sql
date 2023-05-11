CREATE table Artikel(
    sku SERIAL PRIMARY KEY, 
    proizvajalcev_sku TEXT
);

CREATE table Barva(
    koda_barve INTEGER, 
    ime_barve TEXT, 
    sortirni_red_barve INTEGER
 );

CREATE table Barvne_lastnosti(
    koda_proizvajalca TEXT, 
    ime_barve TEXT,
    cmyk TEXT
);

CREATE table Barvni_tip(
    sku SERIAL PRIMARY KEY, 
    tip_barve TEXT
);

CREATE table Cena(
    stil TEXT, 
    cena FLOAT
);

CREATE table Drzava_izvora(
    stil TEXT, 
    izvor TEXT
);

CREATE table Ean(
    sku SERIAL PRIMARY KEY, 
    europska_stevilka_artikla INTEGER
);

CREATE table Firma(
    ime_proizvajalca TEXT, 
    koda_proizvajalca INTEGER
);

CREATE table Je_barve(
    sku SERIAL PRIMARY KEY, 
    barva TEXT
);

CREATE table Je_firme(
    sku SERIAL PRIMARY KEY, 
    koda_proizvajalca INTEGER
);

CREATE table Je_stila(
    sku SERIAL PRIMARY KEY, 
    stil TEXT
);

CREATE table Kolicina_v_kartonu(
    sku SERIAL PRIMARY KEY, 
    stevilo_v_kartonu INTEGER
);

CREATE table Kolicina_v_paketu(
    sku SERIAL PRIMARY KEY, 
    stevilo_v_paketu INTEGER
);

CREATE table Opis_anglescina(
    stil TEXT, 
    ime_anglescina TEXT,
    opis_materiala_anglescina TEXT,
    opis_artikla_anglescina TEXT
);

CREATE table Status(
    sku SERIAL PRIMARY KEY,
    status TEXT
);

CREATE table Stil(
    stil TEXT, 
    ime_1 TEXT
);

CREATE table Stran_kataloga(
    stil TEXT, 
    stran_kataloga TEXT
);

CREATE table Teza(
    sku SERIAL PRIMARY KEY,
    teza FLOAT
);

CREATE table Velikost(
    sku SERIAL PRIMARY KEY,
    velikost TEXT
);

CREATE table Velikostni_tip(
    sku SERIAL PRIMARY KEY,
    tip_velikosti TEXT
);

CREATE table Vrsta_produkta(
    stil TEXT,
    vrsta TEXT
);