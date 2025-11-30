import sqlite3
from sqlite3 import Error

class databaseConn:
    def openConnection(_dbFile):
        print("++++++++++++++++++++++++++++++++++")
        print("Open database: ", _dbFile)

        conn = None
        try:
            conn = sqlite3.connect(_dbFile)
            print("success")
        except Error as e:
            print(e)

        print("++++++++++++++++++++++++++++++++++")

        return conn

    def closeConnection(_conn, _dbFile):
        print("++++++++++++++++++++++++++++++++++")
        print("Close database: ", _dbFile)

        try:
            _conn.close()
            print("success")
        except Error as e:
            print(e)

        print("++++++++++++++++++++++++++++++++++")

