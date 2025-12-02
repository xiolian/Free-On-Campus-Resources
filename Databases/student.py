import json
import sqlite3
from databaseFuncs import databaseConn as dbc
from databaseFuncs import studentFuncs as sf


def main():
    database = r"resource.sqlite"

    # create a database connection
    conn = dbc.openConnection(database)

    # For demo/testing: hardcode a student ID.
    # In a real app, this would come from the frontend / auth layer.
    test_student_id = "U100001"

    with conn:
        aca_advising = sf.viewAcademicAdvising(conn)
        aca_support = sf.viewAcademicSupport(conn)
        funding = sf.viewFunding(conn)
        health_services = sf.viewHealthServices(conn)
        student_supplies = sf.viewStudentSupp(conn)
        tutoring = sf.viewTutoring(conn)

        resources_history = sf.viewResourcesHistory(conn, test_student_id)

        print("\n=== Academic Advising ===")
        print(json.dumps(aca_advising, indent=2))

        print("\n=== Academic Support ===")
        print(json.dumps(aca_support, indent=2))

        print("\n=== Funding ===")
        print(json.dumps(funding, indent=2))

        print("\n=== Health Services ===")
        print(json.dumps(health_services, indent=2))

        print("\n=== Student Supplies ===")
        print(json.dumps(student_supplies, indent=2))

        print("\n=== Tutoring ===")
        print(json.dumps(tutoring, indent=2))

        print(f"\n=== Resource History for student {test_student_id} ===")
        print(json.dumps(resources_history, indent=2))

    dbc.closeConnection(conn, database)


if __name__ == "__main__":
    main()
