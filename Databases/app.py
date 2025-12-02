from flask import Flask, request, jsonify, render_template
from databaseFuncs import databaseConn as dbc
from databaseFuncs import studentFuncs as sf

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path=""
)

conn = dbc.openConnection("resource.sqlite")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/resources-history", methods=["POST"])
def resources_history():
    data = request.get_json(silent=True) or {}
    studentID = data.get("studentID")

    print("DEBUG studentID:", studentID)  # 👈 debug

    if not studentID:
        return jsonify({"error": "studentID is required"}), 400

    history = sf.viewResourcesHistory(conn, studentID)
    print("DEBUG history rows:", len(history))  # 👈 debug

    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
