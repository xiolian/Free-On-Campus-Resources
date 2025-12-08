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
        Shows all students, with 0 counts when they have no records in a category.
        """
        try:
            sql = """
            SELECT
                s.studentID,
                s.studentName,
                COUNT(DISTINCT a.advisor_id)        AS advisor_count,
                COUNT(DISTINCT t.tutoring_id)       AS tutoring_count,
                COUNT(DISTINCT sup.supply_id)       AS supplies_count,
                COUNT(DISTINCT h.health_id)         AS health_count,
                COUNT(DISTINCT asupp.support_id)    AS academic_support_count,
                COUNT(DISTINCT f.funding_id)        AS funding_count,
                (
                    COUNT(DISTINCT a.advisor_id) +
                    COUNT(DISTINCT t.tutoring_id) +
                    COUNT(DISTINCT sup.supply_id) +
                    COUNT(DISTINCT h.health_id) +
                    COUNT(DISTINCT asupp.support_id) +
                    COUNT(DISTINCT f.funding_id)
                ) AS total_resource_count
            FROM Student AS s
            LEFT JOIN AdvisorRecord        AS a     ON a.studentID     = s.studentID
            LEFT JOIN TutoringRecord       AS t     ON t.studentID     = s.studentID
            LEFT JOIN StudentSuppliesRecord AS sup  ON sup.studentID   = s.studentID
            LEFT JOIN HealthRecord         AS h     ON h.studentID     = s.studentID
            LEFT JOIN FundingRecord        AS f     ON f.studentID     = s.studentID
            LEFT JOIN AcademicSupportRecord AS asupp ON asupp.studentID = s.studentID
            GROUP BY s.studentID, s.studentName
            ORDER BY s.studentName;
            """
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    "StudentID":          row[0],
                    "Student Name":       row[1],
                    "Advisor":            row[2],
                    "Tutoring":           row[3],
                    "Supplies":           row[4],
                    "Health":             row[5],
                    "Academic Support":   row[6],
                    "Funding":            row[7],
                    "Total":              row[8],
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

        After slimming Record tables, descriptive columns (name, department, etc.)
        are pulled from the master resource tables via JOIN.
        """
        try:
            cursor = _conn.cursor()

            sql = """
                -- Tutoring
                SELECT
                    'tutoring'              AS category_key,
                    t.tutoring_id           AS resource_id,
                    tr.studentID,
                    tr.studentName,
                    'Tutoring'              AS category,
                    t.subject               AS name,
                    t.department,
                    t.building,
                    t.location,
                    t.weekday,
                    t.start_time,
                    t.end_time,
                    NULL                    AS link
                FROM TutoringRecord tr
                JOIN tutoring t
                  ON t.tutoring_id = tr.tutoring_id
                WHERE tr.studentID = ?

                UNION ALL

                -- Student Supplies
                SELECT
                    'supplies'              AS category_key,
                    ss.supply_id            AS resource_id,
                    ssr.studentID,
                    ssr.studentName,
                    'Supplies'              AS category,
                    ss.item                 AS name,
                    ss.department,
                    ss.building,
                    ss.location,
                    ss.weekday,
                    ss.start_time,
                    ss.end_time,
                    NULL                    AS link
                FROM StudentSuppliesRecord ssr
                JOIN student_supplies ss
                  ON ss.supply_id = ssr.supply_id
                WHERE ssr.studentID = ?

                UNION ALL

                -- Health Services
                SELECT
                    'health'                AS category_key,
                    h.health_id             AS resource_id,
                    hr.studentID,
                    hr.studentName,
                    'Health Service'        AS category,
                    h.service               AS name,
                    NULL                    AS department,
                    NULL                    AS building,
                    h.location,
                    h.weekday,
                    h.start_time,
                    h.end_time,
                    h.link                  AS link
                FROM HealthRecord hr
                JOIN health_services h
                  ON h.health_id = hr.health_id
                WHERE hr.studentID = ?

                UNION ALL

                -- Academic Support
                SELECT
                    'academic_support'      AS category_key,
                    asupp.support_id        AS resource_id,
                    asr.studentID,
                    asr.studentName,
                    'Academic Support'      AS category,
                    asupp.aca_supp_service  AS name,
                    asupp.department,
                    asupp.building,
                    asupp.location,
                    asupp.weekday,
                    asupp.start_time,
                    asupp.end_time,
                    asupp.link              AS link
                FROM AcademicSupportRecord asr
                JOIN academic_support asupp
                  ON asupp.support_id = asr.support_id
                WHERE asr.studentID = ?

                UNION ALL

                -- Advisor assignments
                SELECT
                    'advisor'               AS category_key,
                    adv.advisor_id          AS resource_id,
                    avr.studentID,
                    avr.studentName,
                    'Advisor'               AS category,
                    adv.name                AS name,
                    adv.affiliation         AS department,
                    adv.building,
                    adv.location,
                    NULL                    AS weekday,
                    NULL                    AS start_time,
                    NULL                    AS end_time,
                    adv.link                AS link
                FROM AdvisorRecord avr
                JOIN academic_advising adv
                  ON adv.advisor_id = avr.advisor_id
                WHERE avr.studentID = ?

                UNION ALL

                -- Funding
                SELECT
                    'funding'               AS category_key,
                    f.funding_id            AS resource_id,
                    fr.studentID,
                    fr.studentName,
                    'Funding'               AS category,
                    f.funding_name          AS name,
                    f.department,
                    f.building,
                    f.location,
                    f.weekday,
                    f.start_time,
                    f.end_time,
                    f.link                  AS link
                FROM FundingRecord fr
                JOIN funding f
                  ON f.funding_id = fr.funding_id
                WHERE fr.studentID = ?

                ORDER BY category, name;
            """
            cursor.execute(sql, (studentID,) * 6)
            rows = cursor.fetchall()

            resources = []
            for r in rows:
                resources.append({
                    "category_key": r[0],
                    "resource_id":  r[1],
                    "studentID":    r[2],
                    "studentName":  r[3],
                    "category":     r[4],
                    "name":         r[5],
                    "department":   r[6],
                    "building":     r[7],
                    "location":     r[8],
                    "weekday":      r[9],
                    "start_time":   r[10],
                    "end_time":     r[11],
                    "link":         r[12],
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

    def searchResources(_conn, category_key=None, term=None):
        """
        Return a unified list of resources, optionally filtered by:
          - category_key (e.g. 'tutoring', 'supplies', etc.)
          - term (text search across name/department/building/location/notes)
        """
        term = (term or "").strip().lower()
        category_key = (category_key or "").strip()

        cur = _conn.cursor()

        base_sql = """
        SELECT *
        FROM (
            SELECT
                'supplies'          AS category_key,
                supply_id           AS resource_id,
                'Student Supplies'  AS category,
                item                AS name,
                department,
                building,
                location,
                weekday,
                start_time,
                end_time,
                notes,
                NULL                AS link
            FROM student_supplies

            UNION ALL

            SELECT
                'tutoring'          AS category_key,
                tutoring_id         AS resource_id,
                'Tutoring'          AS category,
                subject             AS name,
                department,
                building,
                location,
                weekday,
                start_time,
                end_time,
                notes,
                NULL                AS link
            FROM tutoring

            UNION ALL

            SELECT
                'health'            AS category_key,
                health_id           AS resource_id,
                'Health Services'   AS category,
                service             AS name,
                NULL                AS department,
                NULL                AS building,
                location,
                weekday,
                start_time,
                end_time,
                NULL                AS notes,
                link
            FROM health_services

            UNION ALL

            SELECT
                'funding'           AS category_key,
                funding_id          AS resource_id,
                'Funding'           AS category,
                funding_name        AS name,
                department,
                building,
                location,
                weekday,
                start_time,
                end_time,
                NULL                AS notes,
                link
            FROM funding

            UNION ALL

            SELECT
                'academic_support'  AS category_key,
                support_id          AS resource_id,
                'Academic Support'  AS category,
                service_name        AS name,
                department,
                building,
                location,
                weekday,
                start_time,
                end_time,
                NULL                AS notes,
                link
            FROM academic_support

            UNION ALL

            SELECT
                'advisor'           AS category_key,
                advisor_id          AS resource_id,
                'Advisor'           AS category,
                name                AS name,
                affiliation         AS department,
                building,
                location,
                NULL                AS weekday,
                NULL                AS start_time,
                NULL                AS end_time,
                NULL                AS notes,
                link
            FROM academic_advising
        ) AS all_resources
        """

        where_clauses = []
        params = []

        if category_key:
            where_clauses.append("category_key = ?")
            params.append(category_key)

        if term:
            like = f"%{term}%"
            where_clauses.append("""
                (
                    LOWER(name)        LIKE ?
                    OR LOWER(COALESCE(department,'')) LIKE ?
                    OR LOWER(COALESCE(building,''))   LIKE ?
                    OR LOWER(COALESCE(location,''))   LIKE ?
                    OR LOWER(COALESCE(notes,''))      LIKE ?
                )
            """)
            params.extend([like, like, like, like, like])

        if where_clauses:
            base_sql += " WHERE " + " AND ".join(where_clauses)

        cur.execute(base_sql, params)
        rows = cur.fetchall()

        cols = [
            "category_key", "resource_id", "category", "name",
            "department", "building", "location",
            "weekday", "start_time", "end_time",
            "notes", "link",
        ]
        return [dict(zip(cols, r)) for r in rows]


