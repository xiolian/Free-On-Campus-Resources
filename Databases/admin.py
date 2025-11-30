import sqlite3
from sqlite3 import Error
from databaseFuncs import databaseConn as dbc
from databaseFuncs import adminFuncs as af

def main():
    database = r"resource.sqlite"

    # create a database connection
    conn = dbc.openConnection(database)
    with conn:
        af.viewAllStudents(conn)
    #     Q2(conn)
    #     Q3(conn)
    #     Q4(conn)
    #     Q5(conn)

    dbc.closeConnection(conn, database)


if __name__ == '__main__':
    main()