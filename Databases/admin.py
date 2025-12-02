import json
import sqlite3
from databaseFuncs import databaseConn as dbc
from databaseFuncs import adminFuncs as af


def main():
    database = r"resource.sqlite"

    # create a database connection
    conn = dbc.openConnection(database)

    with conn:
        # Each function now returns a list[dict], which we can print or
        # later expose via an API.
        all_students = af.viewAllStudents(conn)
        aca_supp_records = af.viewAcaSuppRecord(conn)
        advisor_records = af.viewAdvisorRecord(conn)
        funding_records = af.viewFundingRecord(conn)
        health_records = af.viewHealthRecord(conn)
        supplies_records = af.viewStudentSuppliesRecord(conn)
        tutoring_records = af.viewTutoringRecord(conn)

        # Pretty-print to console (for debugging / CLI use)
        print("\n=== All Students (with resource counts) ===")
        print(json.dumps(all_students, indent=2))

        print("\n=== Academic Support Records ===")
        print(json.dumps(aca_supp_records, indent=2))

        print("\n=== Advisor Records ===")
        print(json.dumps(advisor_records, indent=2))

        print("\n=== Funding Records ===")
        print(json.dumps(funding_records, indent=2))

        print("\n=== Health Records ===")
        print(json.dumps(health_records, indent=2))

        print("\n=== Student Supplies Records ===")
        print(json.dumps(supplies_records, indent=2))

        print("\n=== Tutoring Records ===")
        print(json.dumps(tutoring_records, indent=2))

    dbc.closeConnection(conn, database)


if __name__ == "__main__":
    main()
