from flask import Flask, request, jsonify, render_template
from databaseFuncs import databaseConn as dbc
from databaseFuncs import studentFuncs as sf
from databaseFuncs import adminFuncs as af

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path=""
)

# IMPORTANT: openConnection in databaseFuncs should use check_same_thread=False
conn = dbc.openConnection("resource.sqlite")

# ------------------------------------------------------------
# Admin table configuration
# ------------------------------------------------------------

TABLE_CONFIG = {
    "records": {
        "academic_support": {"table": "AcademicSupportRecord", "pk": "rowid"},
        "advisor":          {"table": "AdvisorRecord",          "pk": "rowid"},
        "funding":          {"table": "FundingRecord",          "pk": "rowid"},
        "health":           {"table": "HealthRecord",           "pk": "rowid"},
        "supplies":         {"table": "StudentSuppliesRecord",  "pk": "rowid"},
        "tutoring":         {"table": "TutoringRecord",         "pk": "rowid"},
    },
    "resources": {
        "academic_support": {"table": "academic_support",   "pk": "support_id"},
        "advisor":          {"table": "academic_advising",  "pk": "advisor_id"},
        "funding":          {"table": "funding",            "pk": "funding_id"},
        "health":           {"table": "health_services",    "pk": "health_id"},
        "supplies":         {"table": "student_supplies",   "pk": "supply_id"},
        "tutoring":         {"table": "tutoring",           "pk": "tutoring_id"},
    },
    # New group for student accounts
    "students": {
        "students":         {"table": "Student",            "pk": "studentID"},
    },
}


def get_table_config(group, category):
    group_cfg = TABLE_CONFIG.get(group)
    if not group_cfg:
        return None
    return group_cfg.get(category)


# ------------------------------------------------------------
# Basic pages
# ------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")


# ------------------------------------------------------------
# Resource catalog for student view
# ------------------------------------------------------------

@app.route("/api/resources", methods=["GET"])
def list_resources():
    category = request.args.get("category")   # e.g. 'tutoring', 'supplies'
    search   = request.args.get("search")     # the typed text

    data = sf.searchResources(conn, category_key=category, term=search)
    return jsonify(data)



# ------------------------------------------------------------
# Helpers for student auth / creation (uses Student.studentPass)
# ------------------------------------------------------------

def ensure_student_with_pass(cur, student_id, student_name, student_pass):
    """
    For checkout:
      - If no Student row: create (id, name, pass)
      - If row exists & studentPass is NULL: set pass & update name
      - If row exists & pass matches: update name
      - If row exists & pass mismatch: return (False, message)
    """
    cur.execute(
        "SELECT studentName, studentPass FROM Student WHERE studentID = ?",
        (student_id,),
    )
    row = cur.fetchone()

    if row is None:
        cur.execute(
            "INSERT INTO Student (studentID, studentName, studentPass) VALUES (?, ?, ?)",
            (student_id, student_name, student_pass),
        )
        return True, None

    existing_name, existing_pass = row

    if existing_pass is None:
        cur.execute(
            "UPDATE Student SET studentName = ?, studentPass = ? WHERE studentID = ?",
            (student_name, student_pass, student_id),
        )
        return True, None

    if existing_pass != student_pass:
        return False, "Incorrect password for this student ID."

    if existing_name != student_name:
        cur.execute(
            "UPDATE Student SET studentName = ? WHERE studentID = ?",
            (student_name, student_id),
        )

    return True, None


# ------------------------------------------------------------
# Insert one record row for a checked-out resource
# ------------------------------------------------------------

def insert_record_for_item(cur, student_id, student_name, category_key, resource_id):
    """Insert one checked-out item into the appropriate *Record table."""
    if category_key == "supplies":
        cur.execute(
            """
            INSERT INTO StudentSuppliesRecord (
                studentID, studentName, supply_id,
                resource_type, item, department,
                building, location, weekday,
                start_time, end_time
            )
            SELECT ?, ?, supply_id,
                   resource_type, item, department,
                   building, location, weekday,
                   start_time, end_time
            FROM student_supplies
            WHERE supply_id = ?
            """,
            (student_id, student_name, resource_id),
        )

    elif category_key == "tutoring":
        cur.execute(
            """
            INSERT INTO TutoringRecord (
                studentID, studentName, tutoring_id,
                resource_type, subject, department,
                building, location, weekday,
                start_time, end_time
            )
            SELECT ?, ?, tutoring_id,
                   resource_type, subject, department,
                   building, location, weekday,
                   start_time, end_time
            FROM tutoring
            WHERE tutoring_id = ?
            """,
            (student_id, student_name, resource_id),
        )

    elif category_key == "health":
        cur.execute(
            """
            INSERT INTO HealthRecord (
                studentID, studentName, health_id,
                health_category, service, location,
                weekday, start_time, end_time, link
            )
            SELECT ?, ?, health_id,
                   health_category, service, location,
                   weekday, start_time, end_time, link
            FROM health_services
            WHERE health_id = ?
            """,
            (student_id, student_name, resource_id),
        )

    elif category_key == "funding":
        cur.execute(
            """
            INSERT INTO FundingRecord (
                studentID, studentName, funding_id,
                funding_type, funding_name, department,
                building, location, weekday,
                start_time, end_time, link
            )
            SELECT ?, ?, funding_id,
                   funding_type, funding_name, department,
                   building, location, weekday,
                   start_time, end_time, link
            FROM funding
            WHERE funding_id = ?
            """,
            (student_id, student_name, resource_id),
        )

    elif category_key == "academic_support":
        cur.execute(
            """
            INSERT INTO AcademicSupportRecord (
                studentID, studentName, support_id,
                aca_supp_service, service_name, department,
                building, location, weekday,
                start_time, end_time, link
            )
            SELECT ?, ?, support_id,
                   aca_supp_service, service_name, department,
                   building, location, weekday,
                   start_time, end_time, link
            FROM academic_support
            WHERE support_id = ?
            """,
            (student_id, student_name, resource_id),
        )

    elif category_key == "advisor":
        cur.execute(
            """
            INSERT INTO AdvisorRecord (
                studentID, studentName, advisor_id,
                name, affiliation, role,
                building, location, link
            )
            SELECT ?, ?, advisor_id,
                   name, affiliation, role,
                   building, location, link
            FROM academic_advising
            WHERE advisor_id = ?
            """,
            (student_id, student_name, resource_id),
        )

    else:
        raise ValueError(f"Unknown category_key: {category_key}")


# ------------------------------------------------------------
# Cart checkout (student side)
# ------------------------------------------------------------

@app.route("/api/cart/checkout", methods=["POST"])
def checkout_cart():
    data = request.get_json(silent=True) or {}
    student_id = (data.get("studentID") or "").strip()
    student_name = (data.get("studentName") or "").strip()
    password = (data.get("password") or "").strip()
    items = data.get("items") or []

    if not student_id or not student_name or not password:
        return jsonify({"success": False, "error": "studentID, studentName, and password are required."}), 400

    if not isinstance(items, list) or not items:
        return jsonify({"success": False, "error": "No items in cart."}), 400

    cur = conn.cursor()
    try:
        ok, err = ensure_student_with_pass(cur, student_id, student_name, password)
        if not ok:
            conn.rollback()
            return jsonify({"success": False, "error": err}), 401

        inserted = 0
        for item in items:
            category_key = item.get("category_key")
            resource_id = item.get("resource_id")
            if not category_key or resource_id is None:
                continue
            insert_record_for_item(cur, student_id, student_name, category_key, resource_id)
            inserted += 1

        conn.commit()
        return jsonify({"success": True, "inserted": inserted})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


# ------------------------------------------------------------
# Student resource history (with password)
# ------------------------------------------------------------

@app.route("/api/resources-history", methods=["POST"])
def resources_history():
    data = request.get_json(silent=True) or {}
    student_id = (data.get("studentID") or "").strip()
    password = (data.get("password") or "").strip()

    if not student_id or not password:
        return jsonify({"error": "studentID and password are required."}), 400

    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT studentName, studentPass FROM Student WHERE studentID = ?",
            (student_id,),
        )
        row = cur.fetchone()
        if row is None:
            conn.rollback()
            return jsonify({"error": "Student ID not found."}), 404

        _, existing_pass = row
        if existing_pass is None:
            cur.execute(
                "UPDATE Student SET studentPass = ? WHERE studentID = ?",
                (password, student_id),
            )
            conn.commit()
        else:
            if existing_pass != password:
                conn.rollback()
                return jsonify({"error": "Incorrect password for this student ID."}), 401
            conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    history = sf.viewResourcesHistory(conn, student_id)
    return jsonify(history)


# ------------------------------------------------------------
# Delete a single history entry (with password)
# ------------------------------------------------------------

@app.route("/api/resources-history/delete", methods=["POST"])
def delete_history_entry():
    data = request.get_json(silent=True) or {}
    student_id = (data.get("studentID") or "").strip()
    password = (data.get("password") or "").strip()
    entry = data.get("entry") or {}

    if not student_id or not password:
        return jsonify({"success": False, "error": "studentID and password are required."}), 400

    category = (entry.get("category") or "").strip()
    name = (entry.get("name") or "").strip()
    department = (entry.get("department") or "").strip()
    building = (entry.get("building") or "").strip()
    location = (entry.get("location") or "").strip()
    weekday = (entry.get("weekday") or "").strip()
    start_time = (entry.get("start_time") or "").strip()
    end_time = (entry.get("end_time") or "").strip()

    if not category or not name:
        return jsonify({"success": False, "error": "category and name are required in entry."}), 400

    cur = conn.cursor()

    # validate password
    try:
        cur.execute("SELECT studentPass FROM Student WHERE studentID = ?", (student_id,))
        row = cur.fetchone()
        if row is None:
            conn.rollback()
            return jsonify({"success": False, "error": "Student ID not found."}), 404

        existing_pass = row[0]
        if existing_pass is None:
            cur.execute(
                "UPDATE Student SET studentPass = ? WHERE studentID = ?",
                (password, student_id),
            )
            conn.commit()
        else:
            if existing_pass != password:
                conn.rollback()
                return jsonify({"success": False, "error": "Incorrect password for this student ID."}), 401
            conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

    # map category name to table + column
    if category == "Tutoring":
        table = "TutoringRecord"
        name_col = "subject"
        extra_cols = ["department", "building", "location", "weekday", "start_time", "end_time"]
    elif category == "Supplies" or category == "Student Supplies":
        table = "StudentSuppliesRecord"
        name_col = "item"
        extra_cols = ["department", "building", "location", "weekday", "start_time", "end_time"]
    elif category == "Health Service" or category == "Health Services":
        table = "HealthRecord"
        name_col = "service"
        extra_cols = ["location", "weekday", "start_time", "end_time"]
    elif category == "Academic Support":
        table = "AcademicSupportRecord"
        name_col = "aca_supp_service"
        extra_cols = ["department", "building", "location", "weekday", "start_time", "end_time"]
    elif category == "Advisor":
        table = "AdvisorRecord"
        name_col = "name"
        extra_cols = ["building", "location"]
    elif category == "Funding":
        table = "FundingRecord"
        name_col = "funding_name"
        extra_cols = ["department", "building", "location", "weekday", "start_time", "end_time"]
    else:
        return jsonify({"success": False, "error": f"Unknown category: {category}"}), 400

    where_clauses = ["studentID = ?", f"{name_col} = ?"]
    params = [student_id, name]

    def add_if(col_name, value):
        if value:
            where_clauses.append(f"{col_name} = ?")
            params.append(value)

    for col in extra_cols:
        if col == "department":
            add_if("department", department)
        elif col == "building":
            add_if("building", building)
        elif col == "location":
            add_if("location", location)
        elif col == "weekday":
            add_if("weekday", weekday)
        elif col == "start_time":
            add_if("start_time", start_time)
        elif col == "end_time":
            add_if("end_time", end_time)

    where_sql = " AND ".join(where_clauses)
    sql = f"""
        DELETE FROM {table}
        WHERE rowid IN (
            SELECT rowid FROM {table}
            WHERE {where_sql}
            LIMIT 1
        )
    """

    try:
        cur.execute(sql, params)
        deleted = cur.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

    if not deleted:
        return jsonify({"success": False, "error": "No matching entry found to delete."}), 404

    return jsonify({"success": True, "deleted": int(deleted)})


# ------------------------------------------------------------
# Most popular resources (student view)
# ------------------------------------------------------------

@app.route("/api/popular-resources", methods=["GET"])
def popular_resources():
    limit = request.args.get("limit", 10, type=int)
    cur = conn.cursor()

    sql = """
    SELECT *
    FROM (
        -- Student Supplies
        SELECT
            'supplies'          AS category_key,
            ss.supply_id        AS resource_id,
            'Student Supplies'  AS category,
            ss.item             AS name,
            ss.department,
            ss.building,
            ss.location,
            ss.weekday,
            ss.start_time,
            ss.end_time,
            NULL                AS link,
            COUNT(ssr.studentID)              AS total_visits,
            COUNT(DISTINCT ssr.studentID)     AS unique_students
        FROM student_supplies ss
        LEFT JOIN StudentSuppliesRecord ssr
          ON ssr.supply_id = ss.supply_id
        GROUP BY
            ss.supply_id, ss.item, ss.department, ss.building,
            ss.location, ss.weekday, ss.start_time, ss.end_time

        UNION ALL

        -- Tutoring
        SELECT
            'tutoring'          AS category_key,
            t.tutoring_id       AS resource_id,
            'Tutoring'          AS category,
            t.subject           AS name,
            t.department,
            t.building,
            t.location,
            t.weekday,
            t.start_time,
            t.end_time,
            NULL                AS link,
            COUNT(tr.studentID)              AS total_visits,
            COUNT(DISTINCT tr.studentID)     AS unique_students
        FROM tutoring t
        LEFT JOIN TutoringRecord tr
          ON tr.tutoring_id = t.tutoring_id
        GROUP BY
            t.tutoring_id, t.subject, t.department, t.building,
            t.location, t.weekday, t.start_time, t.end_time

        UNION ALL

        -- Health Services
        SELECT
            'health'            AS category_key,
            h.health_id         AS resource_id,
            'Health Services'   AS category,
            h.service           AS name,
            NULL                AS department,
            NULL                AS building,
            h.location,
            h.weekday,
            h.start_time,
            h.end_time,
            h.link              AS link,
            COUNT(hr.studentID)              AS total_visits,
            COUNT(DISTINCT hr.studentID)     AS unique_students
        FROM health_services h
        LEFT JOIN HealthRecord hr
          ON hr.health_id = h.health_id
        GROUP BY
            h.health_id, h.service, h.location,
            h.weekday, h.start_time, h.end_time, h.link

        UNION ALL

        -- Funding
        SELECT
            'funding'           AS category_key,
            f.funding_id        AS resource_id,
            'Funding'           AS category,
            f.funding_name      AS name,
            f.department,
            f.building,
            f.location,
            f.weekday,
            f.start_time,
            f.end_time,
            f.link              AS link,
            COUNT(fr.studentID)              AS total_visits,
            COUNT(DISTINCT fr.studentID)     AS unique_students
        FROM funding f
        LEFT JOIN FundingRecord fr
          ON fr.funding_id = f.funding_id
        GROUP BY
            f.funding_id, f.funding_name, f.department, f.building,
            f.location, f.weekday, f.start_time, f.end_time, f.link

        UNION ALL

        -- Academic Support
        SELECT
            'academic_support'  AS category_key,
            a.support_id        AS resource_id,
            'Academic Support'  AS category,
            a.service_name      AS name,
            a.department,
            a.building,
            a.location,
            a.weekday,
            a.start_time,
            a.end_time,
            a.link              AS link,
            COUNT(ar.studentID)              AS total_visits,
            COUNT(DISTINCT ar.studentID)     AS unique_students
        FROM academic_support a
        LEFT JOIN AcademicSupportRecord ar
          ON ar.support_id = a.support_id
        GROUP BY
            a.support_id, a.service_name, a.department, a.building,
            a.location, a.weekday, a.start_time, a.end_time, a.link

        UNION ALL

        -- Advisors
        SELECT
            'advisor'           AS category_key,
            adv.advisor_id      AS resource_id,
            'Advisor'           AS category,
            adv.name            AS name,
            adv.affiliation     AS department,
            adv.building,
            adv.location,
            NULL                AS weekday,
            NULL                AS start_time,
            NULL                AS end_time,
            adv.link            AS link,
            COUNT(avr.studentID)              AS total_visits,
            COUNT(DISTINCT avr.studentID)     AS unique_students
        FROM academic_advising adv
        LEFT JOIN AdvisorRecord avr
          ON avr.advisor_id = adv.advisor_id
        GROUP BY
            adv.advisor_id, adv.name, adv.affiliation,
            adv.building, adv.location, adv.link
    )
    ORDER BY total_visits DESC, unique_students DESC, category, name
    LIMIT ?
    """

    cur.execute(sql, (limit,))
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    result = [dict(zip(cols, r)) for r in rows]
    return jsonify(result)


# ------------------------------------------------------------
# Admin: aggregated student usage table
# ------------------------------------------------------------

@app.route("/api/admin/students", methods=["GET"])
def admin_students():
    data = af.viewAllStudents(conn)
    return jsonify(data)


# ------------------------------------------------------------
# Admin generic manage endpoints (records/resources/students)
# ------------------------------------------------------------

@app.route("/api/admin/manage/<group>/<category>", methods=["GET", "POST"])
def admin_manage_collection(group, category):
    cfg = get_table_config(group, category)
    if not cfg:
        return jsonify({"error": "Unknown group/category"}), 400

    table = cfg["table"]
    pk = cfg["pk"]
    cur = conn.cursor()

    # Special handling for student accounts
    if group == "students" and table == "Student":
        if request.method == "GET":
            cur.execute("SELECT studentID, studentName, studentPass FROM Student ORDER BY studentID")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            result = [dict(zip(cols, r)) for r in rows]
            return jsonify(result)

        # POST -> create or overwrite student row
        data = request.get_json(silent=True) or {}
        student_id = data.get("studentID")
        student_name = data.get("studentName")
        student_pass = data.get("studentPass")

        if not student_id or not student_name:
            return jsonify({"error": "studentID and studentName are required"}), 400

        try:
            cur.execute(
                """
                INSERT INTO Student (studentID, studentName, studentPass)
                VALUES (?, ?, ?)
                ON CONFLICT(studentID) DO UPDATE SET
                    studentName = excluded.studentName,
                    studentPass = excluded.studentPass
                """,
                (student_id, student_name, student_pass),
            )
            conn.commit()
            return jsonify({"success": True, "id": student_id})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500

    # Generic handling for records/resources
    if request.method == "GET":
        if group == "records" and pk == "rowid":
            sql = f"SELECT rowid AS {pk}, * FROM {table}"
        else:
            sql = f"SELECT * FROM {table}"
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        result = [dict(zip(cols, r)) for r in rows]
        return jsonify(result)

    # POST -> create new row (pk typically auto)
    data = request.get_json(silent=True) or {}
    data.pop(pk, None)  # prevent PK injection

    if not data:
        return jsonify({"error": "No data provided"}), 400

    columns = list(data.keys())
    placeholders = ", ".join("?" for _ in columns)
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    values = [data[c] for c in columns]

    try:
        cur.execute(sql, values)
        conn.commit()
        new_id = cur.lastrowid
        return jsonify({"success": True, "id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/admin/manage/<group>/<category>/<pk_value>", methods=["PUT", "DELETE"])
def admin_manage_item(group, category, pk_value):
    cfg = get_table_config(group, category)
    if not cfg:
        return jsonify({"error": "Unknown group/category"}), 400

    table = cfg["table"]
    pk = cfg["pk"]
    cur = conn.cursor()

    # Special handling for student accounts
    if group == "students" and table == "Student":
        student_id_old = pk_value

        if request.method == "DELETE":
            try:
                # delete records first
                for record_table in [
                    "AcademicSupportRecord",
                    "AdvisorRecord",
                    "FundingRecord",
                    "HealthRecord",
                    "StudentSuppliesRecord",
                    "TutoringRecord",
                ]:
                    cur.execute(f"DELETE FROM {record_table} WHERE studentID = ?", (student_id_old,))
                # then delete student row
                cur.execute("DELETE FROM Student WHERE studentID = ?", (student_id_old,))
                conn.commit()
                return jsonify({"success": True})
            except Exception as e:
                conn.rollback()
                return jsonify({"error": str(e)}), 500

        # PUT -> update student row (including optional ID change)
        data = request.get_json(silent=True) or {}
        new_id = data.get("studentID", student_id_old)
        new_name = data.get("studentName")
        new_pass = data.get("studentPass")

        if not new_name:
            # if they didn't send name, keep existing
            cur.execute("SELECT studentName, studentPass FROM Student WHERE studentID = ?", (student_id_old,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "Student not found"}), 404
            existing_name, existing_pass = row
            if new_name is None:
                new_name = existing_name
            if new_pass is None:
                new_pass = existing_pass

        try:
            # update Student row
            cur.execute(
                """
                UPDATE Student
                SET studentID = ?, studentName = ?, studentPass = ?
                WHERE studentID = ?
                """,
                (new_id, new_name, new_pass, student_id_old),
            )

            # cascade ID change into record tables if needed
            if new_id != student_id_old:
                for record_table in [
                    "AcademicSupportRecord",
                    "AdvisorRecord",
                    "FundingRecord",
                    "HealthRecord",
                    "StudentSuppliesRecord",
                    "TutoringRecord",
                ]:
                    cur.execute(
                        f"UPDATE {record_table} SET studentID = ? WHERE studentID = ?",
                        (new_id, student_id_old),
                    )

            conn.commit()
            return jsonify({"success": True})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500

    # Generic handling for records/resources
    if request.method == "DELETE":
        if pk == "rowid":
            sql = f"DELETE FROM {table} WHERE rowid = ?"
        else:
            sql = f"DELETE FROM {table} WHERE {pk} = ?"
        try:
            cur.execute(sql, (pk_value,))
            conn.commit()
            return jsonify({"success": True})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500

    # PUT -> generic update (cannot change PK)
    data = request.get_json(silent=True) or {}
    data.pop(pk, None)

    if not data:
        return jsonify({"error": "No columns to update"}), 400

    columns = list(data.keys())
    set_clause = ", ".join(f"{c} = ?" for c in columns)
    params = [data[c] for c in columns] + [pk_value]

    if pk == "rowid":
        sql = f"UPDATE {table} SET {set_clause} WHERE rowid = ?"
    else:
        sql = f"UPDATE {table} SET {set_clause} WHERE {pk} = ?"

    try:
        cur.execute(sql, params)
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
