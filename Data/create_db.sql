CREATE table Artikel(
    SKU SERIAL PRIMARY KEY,
    Style TEXT,
    Manufacturer TEXT, 
    Name TEXT, 
    Colour TEXT, 
    Size TEXT, 
    Farbtyp TEXT, 
    GroessenTyp TEXT, 
    PCPack INTEGER, 
    PCCarton INTEGER,
    WeightKG FLOAT,
    Status TEXT, 
    EAN INTEGER, 
    ManufacturerSKU TEXT
);