import sqlite3

import pandas as pd


# import io
# import requests
#
# # url = "https://data.statistics.sk/api/SendReport.php?cubeName=om7006rr&lang=sk&fileType=csv"
# s = requests.get(url).content
# c = pd.read_csv(io.StringIO(s.decode('utf-8')))
#
# print(c.head(5))

def save_to_db(df):
    try:
        sqliteConnection = sqlite3.connect('../person_database.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS MunicipalityCodesNumberOfCitizens (
                                            id INTEGER PRIMARY KEY,
                                            Code TEXT,
                                            Year TEXT,
                                            Type TEXT,
                                            number TEXT
                                            );'''
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        df.to_sql('MunicipalityCodesNumberOfCitizens', sqliteConnection, if_exists='replace', index=False)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


df = pd.read_csv('test.csv')
df = df[['Code', 'Year', 'Type', 'number']]
save_to_db(df)
