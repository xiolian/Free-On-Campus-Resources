import sqlite3
from sqlite3 import Error
from databaseFuncs import databaseConn as dbc
from databaseFuncs import studentFuncs as sf

def main():
    database = r"resource.sqlite"

    # create a database connection
    conn = dbc.openConnection(database)
    with conn:
        sf.viewAcademicAdvising(conn)
        sf.viewAcademicSupport(conn)
        sf.viewFunding(conn)
        sf.viewHealthServices(conn)
        sf.viewStudentSupp(conn)
        sf.viewTutoring(conn)

    dbc.closeConnection(conn, database)


if __name__ == '__main__':
    main()