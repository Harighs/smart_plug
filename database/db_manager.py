import sys
sys.path.append('../')
import sqlite3
from sqlite3 import Error
import os
import json

global conn
global cursor
db_name = os.path.join(os.path.dirname(__file__), 'pythonsqlite.db') 

class DatabaseManager:
    def __init__(self):
        print("init called")
        self.create_connection()
        self.create_table()
        # self.insert_datacache_table("2023-09-18 01:00:00", "2023-09-18 02:00:00", "5.50", "100", "0", "0", "0")  # TODO pass it from services
        # self.read_datacache_table()
        # self.delete_datacache_table()

    def create_connection(self):
        try:
            conn = sqlite3.connect(db_name)
            print(sqlite3.version)
        except Error as e:
            print("create_connection", e)
        

    def create_table(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # datacache - table to store the master records from (Awattar service and Smartmeter)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datacache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_timestamp TEXT NOT NULL,
                end_timestamp TEXT NOT NULL,
                awattar_price TEXT NOT NULL,
                smart_meter_consumption TEXT NOT NULL,
                awattar_unit TEXT NOT NULL,
                smart_meter_unit TEXT NOT NULL,
                R1 TEXT NOT NULL,
                R2 TEXT NOT NULL,
                R3 TEXT NOT NULL,
                R4 TEXT NOT NULL,
                R5 TEXT NOT NULL,
                status BOOLEAN,
                mode TEXT NOT NULL
            )
        ''')

        # automode - table to record information for Auto Mode
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automode (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                last_24hrs_usage TEXT NOT NULL,
                times_to_turnon TEXT NOT NULL,
                status BOOLEAN
            )
        ''')

         # automaterelay - table to record information for turn on and turn off
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automaterelay (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_timestamp TEXT NOT NULL,
                end_timestamp TEXT NOT NULL,
                marketprice TEXT NOT NULL,
                unit TEXT NOT NULL,
                triggerstatus BOOLEAN 
            )
        ''')

          # relaysettings - table to record information for turn on and turn off
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relaysettings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                relay1power TEXT NOT NULL,
                relay2power TEXT NOT NULL,
                relay1unit TEXT NOT NULL,
                relay2unit TEXT NOT NULL,
                status BOOLEAN
            )
        ''')

        cursor.close()

    def insert_datacache_table(self, start_datetime, end_datetime, awattar_price, smart_meter_consumption, awattar_unit, smart_meter_unit, R1, R2, R3, R4, R5, status, mode):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO datacache (start_datetime, end_datetime, awattar_price, smart_meter_consumption, awattar_unit, smart_meter_unit, R1, R2, R3, R4, R5, status, mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (start_datetime, end_datetime, awattar_price, smart_meter_consumption, awattar_unit, smart_meter_unit, R1, R2, R3, R4, R5, status, mode))
        conn.commit()
        cursor.close()

    def read_datacache_table(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM datacache")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()

    def read_datacache_withdate_table(self, fromDate, toDate):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT sum(R1) as report1, sum(R2) as report2, sum(R3) as report3, sum(R4) as report4, sum(R5) as report5  FROM datacache WHERE start_timestamp BETWEEN '{fromDate}' AND '{toDate}'")
        rows = cursor.fetchall()

        result_list = []
        for row in rows:
            #print(row)
            result_list.append(row)   
            
        # Convert the list to JSON
        # json_data = json.dumps(result_list, indent=2)

        cursor.close()

        return result_list

    def delete_datacache_table(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM datacache")
        conn.commit()
        cursor.close()

if __name__ == '__main__':
    db = DatabaseManager()