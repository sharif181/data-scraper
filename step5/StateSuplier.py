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
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS StateSuplier (
                                            id INTEGER PRIMARY KEY,
                                            ico TEXT,
                                            Number TEXT
                                            );'''
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        df.to_sql('StateSuplier', sqliteConnection, if_exists='replace', index=False)
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
            '45603731', '36701963', '46505237', '43822177', '47351195', '44135602', '45937273', '36737259', '43953603',
            '46044795', '35900890', '36431788', '46678719', '36498009', '47550848', '47009667', '46245294', '45681058',
            '36821063', '44629362', '36401226', '47521287', '47683449', '46831444',
            '44765835', '44229330', '46860037', '45355568', '36457060', '47781041', '45915768', '47450967', '47248114',
            '36406244']
print(list_ico)

url = "https://www.uvostat.sk/dodavatelia"

driver = webdriver.Chrome('../chromedriver.exe', options=option)
driver.get(url)
sleep(3)

input_element = driver.find_element_by_xpath('//*[@id="listcontractorstable_filter"]/label/input')
rows = []
for ico in list_ico:
    number = 0
    sleep(1)
    input_element.send_keys(ico)
    sleep(2)
    try:
        driver.find_element_by_class_name('dataTables_empty')
    except:
        number = driver.find_element_by_xpath('//*[@id="listcontractorstable"]/tbody/tr[1]/td[6]').text
    rows.append({'ico': ico, 'Number': number})
    input_element.clear()

df = pd.DataFrame(rows)
save_to_db(df)
