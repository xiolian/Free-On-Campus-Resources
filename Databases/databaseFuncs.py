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

class adminFuncs:
    def viewAllStudents(_conn):
        try:
            sql = """
            SELECT
                s.studentID,
                s.studentName,
                COUNT(DISTINCT a.advisor_id) AS advisor_count,
                COUNT(DISTINCT t.tutoring_id) AS tutoring_count,
                COUNT(DISTINCT sup.supply_id) AS supplies_count,
                COUNT(DISTINCT h.health_id) AS health_count,
                COUNT(DISTINCT asupp.support_id) AS academic_support_count,
                COUNT(DISTINCT f.funding_id) AS funding_count,
                (
                COUNT(DISTINCT a.advisor_id) +
                COUNT(DISTINCT t.tutoring_id) +
                COUNT(DISTINCT sup.supply_id) +
                COUNT(DISTINCT h.health_id) +
                COUNT(DISTINCT asupp.support_id) +
                COUNT(DISTINCT f.funding_id)
                ) AS total_resource_count

            FROM Student AS s, AdvisorRecord AS a, TutoringRecord AS t, StudentSuppliesRecord AS sup, HealthRecord AS h, FundingRecord AS f, AcademicSupportRecord AS asupp
            WHERE a.studentID   = s.studentID
            AND t.studentID   = s.studentID
            AND sup.studentID = s.studentID
            AND h.studentID   = s.studentID
            AND asupp.studentID = s.studentID
            AND f.studentID   = s.studentID
            GROUP BY s.studentID, s.studentName;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            output = open('adminOutput/adminCount.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format("studentID", "studentName", "advisor", "tutoring", "supplies", "health", "academic support", "funding", "total resources")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}|{row[8]}\n")
            output.close()
        except Error as e:
            print(e)

class studentFuncs:
    def viewAcademicAdvising(_conn):
        try:
            sql = """
            SELECT *
            FROM academic_advising;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            output = open('studentOutput/acaAdv.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}\n".format("Advisor ID", "Name", "Affiliation", "Role", "Building", "Location", "Link")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}\n")
            output.close()
        except Error as e:
            print(e)

    def viewAcademicSupport(_conn):
        try:
            sql = """
            SELECT *
            FROM academic_support;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            output = open('studentOutput/acaSupp.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format("Academic Support ID", "Academic Support Service", "Service Name", "Department", "Building", "Location", "Weekday", "Start Time", "End Time", "Link")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}|{row[8]}|{row[9]}\n")
            output.close()
        except Error as e:
            print(e)

    def viewFunding(_conn):
        try:
            sql = """
            SELECT *
            FROM funding;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            output = open('studentOutput/funding.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format("Funding ID", "Funding Type", "Funding Name", "Department", "Building", "Location", "Weekday", "Start Time", "End Time", "Link")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}|{row[8]}|{row[9]}\n")
            output.close()
        except Error as e:
            print(e)

    def viewHealthServices(_conn):
        try:
            sql = """
            SELECT *
            FROM health_services;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            output = open('studentOutput/healthServ.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}|{}\n".format("Health ID", "Health Category", "Service", "Location", "Weekday", "Start Time", "End Time", "Link")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}\n")
            output.close()
        except Error as e:
            print(e)

    def viewStudentSupp(_conn):
        try:
            sql = """
            SELECT *
            FROM student_supplies;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            output = open('studentOutput/studentSupp.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format("Supply ID", "Resource Type", "Item", "Department", "Building", "Location", "Limit Info","Weekday", "Start Time", "End Time", "Notes")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}|{row[8]}|{row[9]}|{row[10]}\n")
            output.close()
        except Error as e:
            print(e)

    def viewTutoring(_conn):
        try:
            sql = """
            SELECT *
            FROM tutoring;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            output = open('studentOutput/tutoring.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format("Tutoring ID", "Resource Type", "Subject", "Department", "Building", "Location", "Weekday", "Start Time", "End Time", "Notes")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}|{row[8]}|{row[9]}\n")
            output.close()
        except Error as e:
            print(e)