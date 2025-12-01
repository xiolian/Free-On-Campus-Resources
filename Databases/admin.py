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
        af.viewAcaSuppRecord(conn)
        af.viewAdvisorRecord(conn)
        af.viewFundingRecord(conn)
        af.viewHealthRecord(conn)
        af.viewStudentSuppliesRecord(conn)
        af.viewTutoringRecord(conn)

    dbc.closeConnection(conn, database)


if __name__ == '__main__':
    main()