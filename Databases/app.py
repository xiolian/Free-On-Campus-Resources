from flask import Flask, request, jsonify, render_template
from databaseFuncs import databaseConn as dbc
from databaseFuncs import studentFuncs as sf

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path=""
)

# Single shared connection.
# If you hit thread errors, change databaseConn.openConnection to use:
# sqlite3.connect(_dbFile, check_same_thread=False)
conn = dbc.openConnection("resource.sqlite")

# ------------------------------------------------------------
# Admin table config (for admin.html)
# ------------------------------------------------------------

TABLE_CONFIG = {
    # Per-student history tables (NO explicit PK; we use SQLite rowid)
    "records": {
        "academic_support": {"table": "AcademicSupportRecord", "pk": "rowid"},
        "advisor":          {"table": "AdvisorRecord",          "pk": "rowid"},
        "funding":          {"table": "FundingRecord",          "pk": "rowid"},
        "health":           {"table": "HealthRecord",           "pk": "rowid"},
        "supplies":         {"table": "StudentSuppliesRecord",  "pk": "rowid"},
        "tutoring":         {"table": "TutoringRecord",         "pk": "rowid"},
    },
    # Underlying resource tables (have real PK columns)
    "resources": {
        "academic_support": {"table": "academic_support",   "pk": "support_id"},
        "advisor":          {"table": "academic_advising",  "pk": "advisor_id"},
        "funding":          {"table": "funding",            "pk": "funding_id"},
        "health":           {"table": "health_services",    "pk": "health_id"},
        "supplies":         {"table": "student_supplies",   "pk": "supply_id"},
        "tutoring":         {"table": "tutoring",           "pk": "tutoring_id"},
    }
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
# API: unified list of all available resources (catalog)
# ------------------------------------------------------------

@app.route("/api/resources", methods=["GET"])
def list_resources():
    """
    Return all resources from the master resource tables.

    Optional query param:
      ?category=supplies|tutoring|health|funding|academic_support|advisor
    """
    category_filter = request.args.get("category")

    sql = """
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
        FROM academic_advising;
    """

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    columns = [
        "category_key", "resource_id", "category", "name",
        "department", "building", "location",
        "weekday", "start_time", "end_time",
        "notes", "link",
    ]

    results = [dict(zip(columns, row)) for row in rows]

    if category_filter:
        results = [r for r in results if r["category_key"] == category_filter]

    return jsonify(results)


# ------------------------------------------------------------
# Helpers for Student authentication / creation
# Uses Student(studentID, studentName, studentPass)
# ------------------------------------------------------------

def ensure_student_with_pass(cur, student_id, student_name, student_pass):
    """
    Ensure there is a Student row with this ID and studentPass.

    For CHECKOUT:
      - If no row exists: create one with (studentID, studentName, studentPass).
      - If row exists and studentPass is NULL: first-time setup, set it to the
        provided value and update name.
      - If row exists and studentPass matches: optionally update name.
      - If row exists and studentPass DOES NOT match: return (False, error_msg).
    """
    cur.execute(
        "SELECT studentName, studentPass FROM Student WHERE studentID = ?",
        (student_id,),
    )
    row = cur.fetchone()

    if row is None:
        # Auto-create new student
        cur.execute(
            "INSERT INTO Student (studentID, studentName, studentPass) VALUES (?, ?, ?)",
            (student_id, student_name, student_pass),
        )
        return True, None

    existing_name, existing_pass = row

    # First-time password setup for existing row
    if existing_pass is None:
        cur.execute(
            "UPDATE Student SET studentName = ?, studentPass = ? WHERE studentID = ?",
            (student_name, student_pass, student_id),
        )
        return True, None

    # Password mismatch -> reject
    if existing_pass != student_pass:
        return False, "Incorrect password for this student ID."

    # Password OK; keep name fresh if it changed
    if existing_name != student_name:
        cur.execute(
            "UPDATE Student SET studentName = ? WHERE studentID = ?",
            (student_name, student_id),
        )

    return True, None


# ------------------------------------------------------------
# Helpers to insert checkout rows into *Record tables
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
                start_time, end_time, notes
            )
            SELECT ?, ?, tutoring_id,
                   resource_type, subject, department,
                   building, location, weekday,
                   start_time, end_time, notes
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
# API: checkout selected resources for a student
# ------------------------------------------------------------

@app.route("/api/cart/checkout", methods=["POST"])
def checkout_cart():
    data = request.get_json(silent=True) or {}
    student_id = data.get("studentID", "").strip()
    student_name = data.get("studentName", "").strip()
    # This "password" key is from the front-end; we store/compare it as Student.studentPass
    password = data.get("password", "").strip()
    items = data.get("items", [])

    if not student_id or not student_name or not password:
        return jsonify({
            "success": False,
            "error": "studentID, studentName, and password are required."
        }), 400

    if not isinstance(items, list) or not items:
        return jsonify({
            "success": False,
            "error": "No items in cart."
        }), 400

    cur = conn.cursor()
    try:
        # 1) Ensure / validate Student row (auto-create + password check, using studentPass)
        ok, err = ensure_student_with_pass(cur, student_id, student_name, password)
        if not ok:
            conn.rollback()
            return jsonify({"success": False, "error": err}), 401

        # 2) Insert each cart item into the appropriate *Record table
        inserted = 0
        for item in items:
            category_key = item.get("category_key")
            resource_id = item.get("resource_id")
            if not category_key or resource_id is None:
                continue
            insert_record_for_item(cur, student_id, student_name, category_key, resource_id)
            inserted += 1

        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True, "inserted": inserted})


# ------------------------------------------------------------
# API: student resource / cart history with login
# ------------------------------------------------------------

@app.route("/api/resources-history", methods=["POST"])
def resources_history():
    """
    Returns a student's full resource usage history.

    Expects JSON:
      { "studentID": "...", "password": "..." }

    Behaviour:
      - If Student row doesn't exist -> error.
      - If studentPass is NULL -> set it to the provided one (first login).
      - If password mismatch -> error.
      - If OK -> returns history via studentFuncs.viewResourcesHistory.
    """
    data = request.get_json(silent=True) or {}
    student_id = data.get("studentID", "").strip()
    password = data.get("password", "").strip()

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

        existing_name, existing_pass = row

        # First-time password setup
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

    # Now that password is validated, fetch the history
    history = sf.viewResourcesHistory(conn, student_id)
    return jsonify(history)


# ------------------------------------------------------------
# API: delete a single history entry (with password)
# ------------------------------------------------------------

@app.route("/api/resources-history/delete", methods=["POST"])
def delete_history_entry():
    """
    Delete ONE matching history entry from the appropriate *Record table.

    Expects JSON:
    {
      "studentID": "...",
      "password": "...",
      "entry": {
          "category": "Tutoring" | "Supplies" | "Health Service" |
                      "Academic Support" | "Advisor" | "Funding",
          "name": "...",
          "department": "...",
          "building": "...",
          "location": "...",
          "weekday": "...",
          "start_time": "...",
          "end_time": "...",
          "link": "..."
      }
    }
    """
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

    # Step 1: validate password (do NOT auto-create here)
    try:
        cur.execute(
            "SELECT studentPass FROM Student WHERE studentID = ?",
            (student_id,),
        )
        row = cur.fetchone()
        if row is None:
            conn.rollback()
            return jsonify({"success": False, "error": "Student ID not found."}), 404

        existing_pass = row[0]
        if existing_pass is None:
            # First-time password set via delete is allowed, but unusual;
            # we mimic resources_history behaviour.
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

    # Step 2: map category -> table + "name" column
    if category == "Tutoring":
        table = "TutoringRecord"
        name_col = "subject"
        extra_cols = ["department", "building", "location", "weekday", "start_time", "end_time"]
    elif category == "Supplies":
        table = "StudentSuppliesRecord"
        name_col = "item"
        extra_cols = ["department", "building", "location", "weekday", "start_time", "end_time"]
    elif category == "Health Service":
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

    # Step 3: build WHERE clause using non-empty fields
    where_clauses = ["studentID = ?", f"{name_col} = ?"]
    params = [student_id, name]

    def add_if(col_name, value):
        if value:
            where_clauses.append(f"{col_name} = ?")
            params.append(value)

    # Map extra columns from the generic fields
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
# Admin: read-only summary of all students & counts
# (used by admin.html if you re-enable that section)
# ------------------------------------------------------------

@app.route("/api/admin/students", methods=["GET"])
def admin_students():
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 
            s.studentID,
            s.studentName,
            (SELECT COUNT(*) FROM AcademicSupportRecord WHERE studentID = s.studentID) AS academic_support,
            (SELECT COUNT(*) FROM AdvisorRecord          WHERE studentID = s.studentID) AS advisor,
            (SELECT COUNT(*) FROM FundingRecord          WHERE studentID = s.studentID) AS funding,
            (SELECT COUNT(*) FROM HealthRecord           WHERE studentID = s.studentID) AS health,
            (SELECT COUNT(*) FROM StudentSuppliesRecord  WHERE studentID = s.studentID) AS supplies,
            (SELECT COUNT(*) FROM TutoringRecord         WHERE studentID = s.studentID) AS tutoring
        FROM Student s
        ORDER BY s.studentID, s.studentName;
        """
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    result = [dict(zip(cols, r)) for r in rows]
    return jsonify(result)


# ------------------------------------------------------------
# Admin CRUD APIs for records + resource tables
# (used by admin.html)
# ------------------------------------------------------------

@app.route("/api/admin/manage/<group>/<category>", methods=["GET", "POST"])
def admin_manage_collection(group, category):
    cfg = get_table_config(group, category)
    if not cfg:
        return jsonify({"error": "Unknown group/category"}), 400

    table = cfg["table"]
    pk = cfg["pk"]

    cur = conn.cursor()

    if request.method == "GET":
        # For *Record tables, expose rowid as the pk field
        if group == "records" and pk == "rowid":
            sql = f"SELECT rowid AS {pk}, * FROM {table}"
        else:
            sql = f"SELECT * FROM {table}"

        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        result = [dict(zip(cols, r)) for r in rows]
        return jsonify(result)

    # POST -> create new row
    data = request.get_json(silent=True) or {}
    # Never let the client set the PK directly
    data.pop(pk, None)

    if not data:
        return jsonify({"error": "No data provided"}), 400

    columns = list(data.keys())
    placeholders = ", ".join("?" for _ in columns)
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    values = [data[c] for c in columns]

    cur.execute(sql, values)
    conn.commit()
    new_id = cur.lastrowid

    return jsonify({"success": True, "id": new_id})


@app.route("/api/admin/manage/<group>/<category>/<int:pk_value>",
           methods=["PUT", "DELETE"])
def admin_manage_item(group, category, pk_value):
    cfg = get_table_config(group, category)
    if not cfg:
        return jsonify({"error": "Unknown group/category"}), 400

    table = cfg["table"]
    pk = cfg["pk"]

    cur = conn.cursor()

    if request.method == "DELETE":
        if pk == "rowid":
            sql = f"DELETE FROM {table} WHERE rowid = ?"
        else:
            sql = f"DELETE FROM {table} WHERE {pk} = ?"
        cur.execute(sql, (pk_value,))
        conn.commit()
        return jsonify({"success": True})

    # PUT -> update
    data = request.get_json(silent=True) or {}
    # Do not allow changing PK
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

    cur.execute(sql, params)
    conn.commit()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
