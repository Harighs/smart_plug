import sqlite3
from sqlite3 import Error
import os
from datetime import datetime, timedelta

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
                mode TEXT NULL
            )
        ''')

        # datacache_report - table to store the master records from (Awattar service and Smartmeter) used later for reports
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datacache_report (
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
                mode TEXT NULL
            )
        ''')

        # relaymode_report - table to record information when relay is ON / OFF / AUTO
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relaymode_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                relaynumber INTEGER NOT NULL,
                relayMode TEXT NOT NULL,
                status BOOLEAN
            )
        ''')

        # relaymode_temp - table to record the relay mode temporarly
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS relaymode_temp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            relaynumber INTEGER NOT NULL,
            relayMode TEXT NOT NULL,
            status BOOLEAN
        )
    ''')

        # automode - table to record 24hr auto (E) value 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automode (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                last_24hrs_usage TEXT NOT NULL,
                times_to_turnon TEXT NOT NULL,
                relaynumber INTEGER NOT NULL,   
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
                relaynumber INTEGER NOT NULL,
                triggerstatus BOOLEAN
            )
        ''')

        # automaterelay_report - table to record information for turn on and turn off
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automaterelay_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_timestamp TEXT NOT NULL,
                end_timestamp TEXT NOT NULL,
                marketprice TEXT NOT NULL,
                unit TEXT NOT NULL,
                relaynumber INTEGER NOT NULL,
                triggerstatus BOOLEAN
            )
        ''')

        # relaysettings - table to record app settings
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

        ##### automode TABLE
    def insert_automode(self, last_24hrs_usage, relayNumber, times_to_turnon):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        current_datetime = datetime.now() - timedelta(hours=24)
        current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
        # this data will be inserted every day at 04:00 AM (E-value)
        cursor.execute("INSERT INTO automode(datetime, last_24hrs_usage, relaynumber, times_to_turnon, status) VALUES(?, ?, ?, ?, ?)",
                       (current_datetime, last_24hrs_usage, relayNumber, times_to_turnon, True))
        
        conn.commit()
        cursor.close()


    def read_automode_24hrs_before(self, relayNumber):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        current_datetime = datetime.now() - timedelta(hours=24)
        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_datetime.replace(hour=23, minute=59, second=59, microsecond=99)

        query = f"SELECT times_to_turnon FROM automode WHERE relaynumber=? AND status=1 AND datetime BETWEEN '{start_of_day}' AND '{end_of_day}' ORDER BY id DESC;"
        cursor.execute(query, (relayNumber,))
        
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            result_list.append(row)
        
        cursor.close()
        return result_list
    
    def read_automode_48hrs_before(self, relayNumber):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        current_datetime = datetime.now() - timedelta(hours=48)
        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_datetime.replace(hour=23, minute=59, second=59, microsecond=99)

        query = f"SELECT times_to_turnon FROM automode WHERE relaynumber=? AND status=1 AND datetime BETWEEN '{start_of_day}' AND '{end_of_day}';"
        cursor.execute(query, (relayNumber,))
        
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            result_list.append(row)
        
        cursor.close()
        return result_list


        ##### relaymode_report, relaymode_temp TABLE

    def insert_relaymode_report(self, relayNumber, relayMode):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # this below entry is to track when the relay is turned on or off or auto mode
        # mainly for future record purpose
        cursor.execute("INSERT INTO relaymode_report(datetime, relaynumber, relayMode, status) VALUES(?, ?, ?, ?)",
                       (datetime.now(), relayNumber, relayMode, True))
        
        conn.commit()
        cursor.close()

    def insert_relaymode_temp(self, relayNumber, relayMode):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # this below entry is to temporary purpose to handle the status of the relays
        cursor.execute("INSERT INTO relaymode_temp(datetime, relaynumber, relayMode, status) VALUES(?, ?, ?, ?)",
                        (datetime.now(), relayNumber, relayMode, True))

        conn.commit()
        cursor.close()


    def read_relay_while_onauto_temp(self, relayNumber):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Get the current datetime
        current_datetime = datetime.now()

        # Calculate a datetime that is 30 minutes ago
        datetime_30_minutes_ago = current_datetime - timedelta(minutes=30)

        # Calculate a datetime that is 1 hour in the future
        datetime_1_hour_in_future = current_datetime + timedelta(hours=1)

        query = f"SELECT * FROM relaymode_temp WHERE relaynumber=? AND status=1 AND datetime BETWEEN '{datetime_30_minutes_ago}' AND '{datetime_1_hour_in_future}';"
        cursor.execute(query, (relayNumber,))
        
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            # print(row)
            result_list.append(row)
        
        cursor.close()
        return result_list
    

    def read_relaymode_temp(self, relayNumber):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
    
        query = "SELECT * FROM relaymode_temp WHERE relaynumber=? AND status=1 ORDER BY id DESC"
        cursor.execute(query, (relayNumber,))
        
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            # print(row)
            result_list.append(row)
        
        cursor.close()
        return result_list
    
    def delete_relaymode_temp(self, relayNumber):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print("delete called")
        query = "DELETE FROM relaymode_temp WHERE relaynumber=?"
        cursor.execute(query, (relayNumber,))
        conn.commit()
        cursor.close()

        ##### relaysettings TABLE

    def insert_relaysettings_table(self, relay1Power, relay2Power):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM relaysettings")
        cursor.execute(
            "INSERT INTO relaysettings(datetime, relay1power, relay2power, relay1unit, relay2unit,status) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now(), relay1Power, relay2Power, "kWh", "kWh", True))
        conn.commit()
        cursor.close()


    def read_relaysettings_table(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("select * from relaysettings")
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            result_list.append(row)
        cursor.close()
        return result_list


        ##### DATACACHE TABLE

    def insert_datacache_table(self, start_datetime, end_datetime, awattar_price, smart_meter_consumption, awattar_unit,
                               smart_meter_unit, R1, R2, R3, R4, R5, status, mode):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO datacache (start_datetime, end_datetime, awattar_price, smart_meter_consumption, awattar_unit, smart_meter_unit, R1, R2, R3, R4, R5, status, mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (start_datetime, end_datetime, awattar_price, smart_meter_consumption, awattar_unit, smart_meter_unit, R1,
             R2, R3, R4, R5, status, mode))
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


    def read_datacache_last_24hrs_consumption(self):
        current_datetime = datetime.now() - timedelta(hours=24)
        print(current_datetime.date())
        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_datetime.replace(hour=23, minute=59, second=59, microsecond=99)

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT sum(smart_meter_consumption) as consumption, smart_meter_unit as unit FROM datacache WHERE start_timestamp BETWEEN '{start_of_day}' AND '{end_of_day}'")
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            result_list.append(row)
        cursor.close()
        return result_list
    

    def read_datacache_last_48hrs_consumption(self):
        current_datetime = datetime.now() - timedelta(hours=48)
        print(current_datetime.date())
        start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_datetime.replace(hour=23, minute=59, second=59, microsecond=99)

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT sum(smart_meter_consumption) as consumption, smart_meter_unit as unit FROM datacache WHERE start_timestamp BETWEEN '{start_of_day}' AND '{end_of_day}'")
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            result_list.append(row)
        cursor.close()
        return result_list


    def read_datacache_withdate_table(self, fromDate, toDate):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT sum(R1) as report1, sum(R2) as report2, sum(R3) as report3, sum(R4) as report4, sum(R5) as report5  FROM datacache WHERE start_timestamp BETWEEN '{fromDate}' AND '{toDate}'")
        rows = cursor.fetchall()

        result_list = []
        for row in rows:
            # print(row)
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
