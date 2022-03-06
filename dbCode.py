import sqlite3

try:
    sqliteConnection = sqlite3.connect('person_database.db')
    sqlite_create_table_query = '''CREATE TABLE FinancialStatements (
                                        id INTEGER PRIMARY KEY,
                                        skNace TEXT,
                                        sidlo TEXT,
                                        zdrojDat TEXT,
                                        ico TEXT,
                                        dic TEXT,
                                        nazovUJ TEXT,
                                        mesto TEXT,
                                        ulica TEXT,
                                        psc TEXT,
                                        datumPoslednejUpravy TEXT,
                                        datumZalozenia TEXT,
                                        datumZrusenia TEXT,
                                        pravnaForma TEXT,
                                        velkostOrganizacie TEXT,
                                        druhVlastnictva TEXT,
                                        kraj TEXT,
                                        okres TEXT,
                                        konsolidovana TEXT);'''
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("The SQLite connection is closed")