import sqlite3
import pandas as pd
import xml.etree.ElementTree as et
import datetime
from dateutil.relativedelta import relativedelta


def save_to_db(df):
    try:
        sqliteConnection = sqlite3.connect('../person_database.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS VatRegistration (
                                            id INTEGER PRIMARY KEY,
                                            ico TEXT,
                                            DRUH_REG_DPH TEXT,
                                            DATUM_REG TEXT,
                                            YearsOfRegistration TEXT
                                            );'''
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        df.to_sql('VatRegistration', sqliteConnection, if_exists='replace', index=False)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def parse_XML(xml_file, df_cols):
    """Parse the input XML file and store the result in a pandas
    DataFrame with the given columns.

    The first element of df_cols is supposed to be the identifier
    variable, which is an attribute of each node element in the
    XML data; other features will be parsed from the text content
    of each sub-element.
    """

    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []

    for node in xroot[1]:
        # print(node.find(df_cols[0]).text)
        try:
            if node.find(df_cols[0]).text:
                ico = node.find(df_cols[0]).text
            else:
                ico = None

            if node.find(df_cols[1]).text:
                druh_reg_dph = node.find(df_cols[1]).text
            else:
                druh_reg_dph = None

            if node.find(df_cols[2]).text:
                datum_reg = node.find(df_cols[2]).text
                date_time_obj = datetime.datetime.strptime(datum_reg, '%d.%m.%Y')
                rd = relativedelta(datetime.date.today(), date_time_obj.date())
                YearsOfRegistration = rd.years
            else:
                datum_reg = None
        except:
            pass
        rows.append({"ico": ico, "DRUH_REG_DPH": druh_reg_dph, "DATUM_REG": datum_reg,
                     "YearsOfRegistration": YearsOfRegistration})

    return rows


rows = parse_XML('ds_dphs.xml', ['ICO', 'DRUH_REG_DPH', 'DATUM_REG'])
df = pd.DataFrame(rows)
save_to_db(df)
