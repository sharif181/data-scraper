import sqlite3
import pandas as pd


def save_to_db(df):
    try:
        sqliteConnection = sqlite3.connect('../person_database.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS MunicipalityCodesSelfEmployedPersons (
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
        df.to_sql('MunicipalityCodesSelfEmployedPersons', sqliteConnection, if_exists='replace', index=False)
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
