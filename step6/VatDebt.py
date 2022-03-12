import sqlite3
import pandas as pd
import xml.etree.ElementTree as et


def save_to_db(df):
    try:
        sqliteConnection = sqlite3.connect('../person_database.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS VatDebt (
                                            id INTEGER PRIMARY KEY,
                                            ico TEXT,
                                            CIASTKA TEXT
                                            );'''
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        df.to_sql('VatDebt', sqliteConnection, if_exists='replace', index=False)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def parse_XML(xml_file, df_cols):
    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []

    for node in xroot[1]:
        # print(node.find(df_cols[0]).text)
        try:
            # if node.find(df_cols[0]).text:
            #     ico = node.find(df_cols[0]).text
            # else:
            #     ico = None

            if node.find(df_cols[1]).text:
                ciastka = node.find(df_cols[1]).text
            else:
                ciastka = None

        except:
            pass
        rows.append({"CIASTKA": ciastka})

    return rows


rows = parse_XML('ds_dsdd.xml', ['ICO', 'CIASTKA'])
df = pd.DataFrame(rows)
save_to_db(df)
