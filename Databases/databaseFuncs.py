import sqlite3
from sqlite3 import Error


class databaseConn:
    def openConnection(_dbFile):
        print("++++++++++++++++++++++++++++++++++")
        print("Open database: ", _dbFile)

        conn = None
        try:
            # allow the same connection object to be used from multiple threads
            conn = sqlite3.connect(_dbFile, check_same_thread=False)
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
    def viewAcaSuppRecord(_conn):
        """
        Return all rows from AcademicSupportRecord as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM AcademicSupportRecord;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "studentID": row[0],
                    "studentName": row[1],
                    "support_id": row[2],
                    "support_service": row[3],
                    "service_name": row[4],
                    "department": row[5],
                    "building": row[6],
                    "location": row[7],
                    "weekday": row[8],
                    "start_time": row[9],
                    "end_time": row[10],
                    "link": row[11],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewTutoringRecord(_conn):
        """
        Return all rows from TutoringRecord as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM TutoringRecord;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "studentID": row[0],
                    "studentName": row[1],
                    "tutoring_id": row[2],
                    "resource_type": row[3],
                    "subject": row[4],
                    "department": row[5],
                    "building": row[6],
                    "location": row[7],
                    "weekday": row[8],
                    "start_time": row[9],
                    "end_time": row[10],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewStudentSuppliesRecord(_conn):
        """
        Return all rows from StudentSuppliesRecord as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM StudentSuppliesRecord;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "studentID": row[0],
                    "studentName": row[1],
                    "supply_id": row[2],
                    "resource_type": row[3],
                    "item": row[4],
                    "role": row[5],
                    "building": row[6],
                    "location": row[7],
                    "link": row[8],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewHealthRecord(_conn):
        """
        Return all rows from HealthRecord as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM HealthRecord;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "studentID": row[0],
                    "studentName": row[1],
                    "health_id": row[2],
                    "health_category": row[3],
                    "health_service": row[4],
                    "location": row[5],
                    "weekday": row[6],
                    "start_time": row[7],
                    "end_time": row[8],
                    "link": row[9],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewAdvisorRecord(_conn):
        """
        Return all rows from AdvisorRecord as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM AdvisorRecord;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "studentID": row[0],
                    "studentName": row[1],
                    "advisor_id": row[2],
                    "name": row[3],
                    "affiliation": row[4],
                    "role": row[5],
                    "building": row[6],
                    "location": row[7],
                    "link": row[8],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewFundingRecord(_conn):
        """
        Return all rows from FundingRecord as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM FundingRecord;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "studentID": row[0],
                    "studentName": row[1],
                    "funding_id": row[2],
                    "funding_type": row[3],
                    "funding_name": row[4],
                    "department": row[5],
                    "building": row[6],
                    "location": row[7],
                    "weekday": row[8],
                    "start_time": row[9],
                    "end_time": row[10],
                    "link": row[11],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewAllStudents(_conn):
        """
        Return aggregate resource counts per student as a list of dicts.
        """
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
            FROM Student AS s, AdvisorRecord AS a, TutoringRecord AS t,
                 StudentSuppliesRecord AS sup, HealthRecord AS h,
                 FundingRecord AS f, AcademicSupportRecord AS asupp
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

            results = []
            for row in rows:
                results.append({
                    "studentID": row[0],
                    "studentName": row[1],
                    "advisor_count": row[2],
                    "tutoring_count": row[3],
                    "supplies_count": row[4],
                    "health_count": row[5],
                    "academic_support_count": row[6],
                    "funding_count": row[7],
                    "total_resource_count": row[8],
                })
            return results
        except Error as e:
            print(e)
            return []


class studentFuncs:

    def registerStudent(_conn, studentID, studentName):
        """
        Insert a new student and return a JSON-friendly status dict.
        """
        try:
            cursor = _conn.cursor()
            sql = "INSERT INTO Student (studentID, studentName) VALUES (?, ?);"
            cursor.execute(sql, (studentID, studentName))
            _conn.commit()
            return {"success": True, "studentID": studentID, "studentName": studentName}
        except Error as e:
            print(e)
            return {"success": False, "error": str(e)}

    def viewResourcesHistory(_conn, studentID):
        """
        Returns all resources a student has obtained, unified across all *Record tables,
        as a JSON-serializable list of dictionaries.
        """
        try:
            cursor = _conn.cursor()

            sql = """
                -- Tutoring
                SELECT studentID,
                       studentName,
                       'Tutoring' AS category,
                       subject     AS name,
                       department,
                       building,
                       location,
                       weekday,
                       start_time,
                       end_time,
                       NULL AS link
                FROM TutoringRecord
                WHERE studentID = ?

                UNION ALL

                -- Student Supplies
                SELECT studentID,
                       studentName,
                       'Supplies'  AS category,
                       item        AS name,
                       department,
                       building,
                       location,
                       weekday,
                       start_time,
                       end_time,
                       NULL AS link
                FROM StudentSuppliesRecord
                WHERE studentID = ?

                UNION ALL

                -- Health Services
                SELECT studentID,
                       studentName,
                       'Health Service' AS category,
                       service          AS name,
                       NULL AS department,
                       NULL AS building,
                       location,
                       weekday,
                       start_time,
                       end_time,
                       link
                FROM HealthRecord
                WHERE studentID = ?

                UNION ALL

                -- Academic Support
                SELECT studentID,
                       studentName,
                       'Academic Support' AS category,
                       aca_supp_service   AS name,
                       department,
                       building,
                       location,
                       weekday,
                       start_time,
                       end_time,
                       link
                FROM AcademicSupportRecord
                WHERE studentID = ?

                UNION ALL

                -- Advisor assignments
                SELECT studentID,
                       studentName,
                       'Advisor' AS category,
                       name      AS name,
                       NULL AS department,
                       building,
                       location,
                       NULL AS weekday,
                       NULL AS start_time,
                       NULL AS end_time,
                       link
                FROM AdvisorRecord
                WHERE studentID = ?

                UNION ALL

                -- Funding
                SELECT studentID,
                       studentName,
                       'Funding' AS category,
                       funding_name AS name,
                       department,
                       building,
                       location,
                       weekday,
                       start_time,
                       end_time,
                       link
                FROM FundingRecord
                WHERE studentID = ?

                ORDER BY category, name;
            """
            cursor.execute(sql, (studentID,) * 6)
            rows = cursor.fetchall()

            resources = []
            for r in rows:
                resources.append({
                    "studentID": r[0],
                    "studentName": r[1],
                    "category": r[2],
                    "name": r[3],
                    "department": r[4],
                    "building": r[5],
                    "location": r[6],
                    "weekday": r[7],
                    "start_time": r[8],
                    "end_time": r[9],
                    "link": r[10],
                })
            return resources
        except Error as e:
            print(e)
            return []

    def viewAcademicAdvising(_conn):
        """
        Return all academic advising options as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM academic_advising;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "advisor_id": row[0],
                    "name": row[1],
                    "affiliation": row[2],
                    "role": row[3],
                    "building": row[4],
                    "location": row[5],
                    "link": row[6],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewAcademicSupport(_conn):
        """
        Return all academic support resources as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM academic_support;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "support_id": row[0],
                    "support_service": row[1],
                    "service_name": row[2],
                    "department": row[3],
                    "building": row[4],
                    "location": row[5],
                    "weekday": row[6],
                    "start_time": row[7],
                    "end_time": row[8],
                    "link": row[9],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewFunding(_conn):
        """
        Return all funding resources as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM funding;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "funding_id": row[0],
                    "funding_type": row[1],
                    "funding_name": row[2],
                    "department": row[3],
                    "building": row[4],
                    "location": row[5],
                    "weekday": row[6],
                    "start_time": row[7],
                    "end_time": row[8],
                    "link": row[9],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewHealthServices(_conn):
        """
        Return all health services as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM health_services;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "health_id": row[0],
                    "health_category": row[1],
                    "service": row[2],
                    "location": row[3],
                    "weekday": row[4],
                    "start_time": row[5],
                    "end_time": row[6],
                    "link": row[7],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewStudentSupp(_conn):
        """
        Return all student supplies as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM student_supplies;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "supply_id": row[0],
                    "resource_type": row[1],
                    "item": row[2],
                    "department": row[3],
                    "building": row[4],
                    "location": row[5],
                    "limit_info": row[6],
                    "weekday": row[7],
                    "start_time": row[8],
                    "end_time": row[9],
                    "notes": row[10],
                })
            return results
        except Error as e:
            print(e)
            return []

    def viewTutoring(_conn):
        """
        Return all tutoring options as a list of dicts.
        """
        try:
            sql = """
            SELECT *
            FROM tutoring;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "tutoring_id": row[0],
                    "resource_type": row[1],
                    "subject": row[2],
                    "department": row[3],
                    "building": row[4],
                    "location": row[5],
                    "weekday": row[6],
                    "start_time": row[7],
                    "end_time": row[8],
                    "notes": row[9],
                })
            return results
        except Error as e:
            print(e)
            return []
