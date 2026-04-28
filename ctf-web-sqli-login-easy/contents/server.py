import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory, session

DB_PATH = "/tmp/lab_sqli_login_easy.db"
FLAG_PATH = "/opt/flag/flag.txt"

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET", "altair-sqli-login-easy-secret")


def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute(
        """
        CREATE TABLE users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL,
          password TEXT NOT NULL,
          role TEXT NOT NULL
        )
        """
    )
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("admin", "S3cur3-NeverGuess", "admin"),
    )
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("guest", "guest", "user"),
    )
    conn.commit()
    conn.close()


@app.get("/")
def index():
    return send_from_directory("public", "index.html")


@app.get("/public/<path:filename>")
def public_files(filename):
    return send_from_directory("public", filename)


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", ""))
    password = str(data.get("password", ""))

    query = (
        "SELECT id, username, role FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    conn = db_conn()
    row = conn.execute(query).fetchone()
    conn.close()

    if row is None:
        session.clear()
        return jsonify({"ok": False, "error": "Invalid credentials"}), 401

    session["user"] = row["username"]
    session["role"] = row["role"]
    return jsonify({"ok": True, "user": row["username"], "role": row["role"]})


@app.get("/api/me")
def me():
    return jsonify(
        {
            "ok": True,
            "user": session.get("user"),
            "role": session.get("role"),
        }
    )


@app.get("/api/flag")
def flag():
    if session.get("role") != "admin":
        return jsonify({"ok": False, "error": "Admin only"}), 403
    with open(FLAG_PATH, "r", encoding="utf-8") as f:
        return jsonify({"ok": True, "flag": f.read().strip()})


@app.get("/api/hint")
def hint():
    return jsonify(
        {
            "ok": True,
            "message": "Login is backed by SQLite and built from raw user input.",
        }
    )


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
