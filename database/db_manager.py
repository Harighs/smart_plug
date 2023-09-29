import sqlite3
from sqlite3 import Error

conn = None
cursor = None
db_name = "pythonsqlite.db"

"""
Created a Sqlite3 local database to store our datasets
    - datacache: table has awattar price and smart meter consumption infos
    - 
"""

def create_connection():
    try:
        conn = sqlite3.connect(db_name)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datacache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_datetime TEXT NOT NULL,
            end_datetime TEXT NOT NULL,
            awattar_price TEXT NOT NULL,
            smart_meter_consumption TEXT NOT NULL,
            awattar_unit TEXT NOT NULL,
            smart_meter_unit TEXT NOT NULL,
            status BOOLEAN
        )
    ''')
    cursor.close()

def insert_table(start_datetime, end_datetime, awattar_price, smart_meter_consumption):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO datacache (start_datetime, end_datetime, awattar_price, smart_meter_consumption, awattar_unit, smart_meter_unit, status) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (start_datetime, end_datetime, awattar_price, smart_meter_consumption, '€', 'Eur/MWh', 'true'))
    conn.commit()
    cursor.close()

def read_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datacache")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()

def delete_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datacache")
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    create_connection()
    create_table()
    insert_table("2023-09-18 01:00:00", "2023-09-18 02:00:00", "5.50", "100") # TODO pass it from services
    read_table()
    #delete_table()