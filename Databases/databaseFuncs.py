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

            output = open('output/adminCount.out', 'w')
            header = "{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format("studentID", "studentName", "advisor", "tutoring", "supplies", "health", "academic support", "funding", "total resources")
            output.write(header)
            for row in rows:
                output.write(f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}|{row[6]}|{row[7]}|{row[8]}\n")
            output.close()
        except Error as e:
            print(e)