import sqlite3
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS InsuranceUnion (
                                            id INTEGER PRIMARY KEY,
                                            ico TEXT,
                                            Amount TEXT
                                            );'''
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        df.to_sql('InsuranceUnion', sqliteConnection, if_exists='replace', index=False)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


print('getting all ico')
# list_ico = select_all_tasks()
# list_ico = ['45886814', '36443565', '47568097', '44961669', '47533137', '35896451', '48246140', '44432739', '36442500',
#             '45603731', '36701963']
list_ico = ['34270108', '45886814']
# print(list_ico)
rows = []
url = "https://portal.unionzp.sk/onlinepobocka/pub/zoznam-dlznikov"

driver = webdriver.Chrome('../chromedriver.exe')

for ico in list_ico:
    try:
        driver.get(url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="j_idt125:vyhladajPodla_input"]'))
        )
        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="j_idt125:j_idt130"]'))
        )
        element.send_keys(ico)
        sleep(2)
        btn.click()
        sleep(4)
        output = driver.find_element_by_xpath('//*[@id="j_idt125:table_data"]/tr/td[3]/font/font')
        print(output)
        element.clear()

    except:
        print('amount 0')
        pass

# df = pd.DataFrame(rows)
# save_to_db(df)
