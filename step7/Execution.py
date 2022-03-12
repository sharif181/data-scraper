import sqlite3
import pandas as pd
from time import sleep
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument('headless')


def select_all_tasks():
    try:
        conn = sqlite3.connect('../person_database.db')
        cur = conn.cursor()
        cur.execute("SELECT ICO FROM PersonData")
        rows = cur.fetchall()
        list = []
        for row in rows:
            list.append(row[0])
        conn.close()
        return list
    except:
        conn.close()
        return []


def save_to_db(df):
    try:
        sqliteConnection = sqlite3.connect('../person_database.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS Execution (
                                            id INTEGER PRIMARY KEY,
                                            ico TEXT,
                                            ExecutionInfo TEXT,
                                            Statement TEXT
                                            );'''
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        df.to_sql('Execution', sqliteConnection, if_exists='replace', index=False)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


print('getting all ico')
# list_ico = select_all_tasks()
list_ico = ['45886814', '36443565', '47568097', '44961669', '47533137', '35896451', '48246140', '44432739', '36442500',
            '45603731', '36701963']
# print(list_ico)

url = "https://obcan.justice.sk/poverenia/rozsirene-vyhladavanie/hladaj?searchType=po&ico="

driver = webdriver.Chrome('../chromedriver.exe', options=option)
rows = []
for ico in list_ico:
    mainUrl = url + ico
    driver.get(mainUrl)
    sleep(2)
    try:
        elm = driver.find_element_by_xpath('//*[@id="povereniaList"]/div/div[1]/div/span')
        rows.append({'ico': ico, 'ExecutionInfo': None, 'Statement': None})
    except:
        col_10 = driver.find_elements_by_class_name('col-sm-10')
        col_2_tags = driver.find_elements_by_class_name('col-sm-2')
        c2 = []
        for col2 in col_2_tags:
            if col2.text not in ['IČO', 'Názov']:
                c2.append(col2.text)

        for col10, col2 in zip(col_10, c2):
            rows.append({'ico': ico, 'ExecutionInfo': col10.text.replace('Číslo poverenia: ', ''), 'Statement': col2})
df = pd.DataFrame(rows)
save_to_db(df)