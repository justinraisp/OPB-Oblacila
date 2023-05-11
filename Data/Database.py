class Repo:   
    def df_to_sql_create(self, df: DataFrame, name: str, add_serial=False, use_camel_case=True) -> str:
        """
        Funkcija ustvari in izvede sql stavek za create table na podlagi podanega pandas DataFrame-a. 
        df: DataFrame za katerega zgradimo sql stavek
        name: ime nastale tabele v bazi
        add_serial: opcijski parameter, ki nam pove ali želimo dodat serial primary key stolpec
        """

        # dobimo slovar stolpcev in njihovih tipov
        cols = dict(df.dtypes)

        cols_sql = ""

        # dodamo serial primary key
        if add_serial: cols_sql += 'Id SERIAL PRIMARY KEY,\n'
        
        # dodamo ostale stolpce
        # tukaj bi stolpce lahko še dodatno filtrirali, preimenovali, itd.
        cols_sql += ",\n".join([self.col_to_sql(col, str(typ), use_camel_case=use_camel_case) for col, typ in cols.items()])


        # zgradimo končen sql stavek
        sql = f'''CREATE TABLE IF NOT EXISTS {name}(
            {cols_sql}
        )'''
