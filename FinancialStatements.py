import requests
import json
import sqlite3

codes = [101, 102, 105, 109, 110, 112]
date = "1999-01-01"


def insertMultipleRecords(record):
    try:
        sqliteConnection = sqlite3.connect('person_database.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query = """INSERT INTO FinancialStatements
                          (id, skNace, sidlo, zdrojDat, ico, dic, nazovUJ, mesto, ulica, psc, datumPoslednejUpravy,
                          datumZalozenia, datumZrusenia, pravnaForma, velkostOrganizacie, druhVlastnictva, kraj, okres,
                          konsolidovana) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        cursor.execute(sqlite_insert_query, record)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("insert multiple records into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


for code in codes:
    existujeDalsieId = True
    hasNext = False
    while existujeDalsieId:
        if hasNext:
            url = f'https://www.registeruz.sk/cruz-public/api/uctovne-jednotky?zmenene-od={date}&pravnaforma={code}&max-zaznamov=10000&pokracovat-za-id={lid}'
        else:
            url = f'https://www.registeruz.sk/cruz-public/api/uctovne-jednotky?zmenene-od={date}&pravnaforma={code}&max-zaznamov=10000'
        res = requests.get(url=url)
        response = json.loads(res.content)
        ids = response.get('id')
        existujeDalsieId = response.get('existujeDalsieId')
        if existujeDalsieId:
            hasNext = True
        lid = ""

        for id in ids:
            lid = id
            data_url = f'https://www.registeruz.sk/cruz-public/api/uctovna-jednotka?id={id}'
            try:
                data_res = requests.get(data_url)
                data = json.loads(data_res.content)
                record = (data.get('id'), data.get('skNace'), data.get('sidlo'), data.get('zdrojDat'), data.get('ico'),
                          data.get('dic'), data.get('nazovUJ'), data.get('mesto'), data.get('ulica'), data.get('psc'),
                          data.get('datumPoslednejUpravy'), data.get('datumZalozenia'), data.get('datumZrusenia'),
                          data.get('pravnaForma'), data.get('velkostOrganizacie'), data.get('druhVlastnictva'),
                          data.get('kraj'), data.get('okres'), data.get('konsolidovana'))
                insertMultipleRecords(record)
            except:
                pass
