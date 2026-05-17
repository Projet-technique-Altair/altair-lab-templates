import os
import sqlite3
import threading
from flask import Flask, jsonify, request, session
from werkzeug.serving import make_server
import requests

DB_PATH = "/tmp/borealis.db"
FLAG = os.getenv("ALTAIR_FLAG_STEP_6", "ALTAIR{borealis_control_plane_root}")

public_app = Flask(__name__)
public_app.secret_key = os.getenv("APP_SECRET", "borealis-dev-secret")
internal_app = Flask("internal")


def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS projects")
    cur.execute("DROP TABLE IF EXISTS secrets")
    cur.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, password TEXT, role TEXT)"
    )
    cur.execute(
        "CREATE TABLE projects (id INTEGER PRIMARY KEY, name TEXT, owner TEXT)"
    )
    cur.execute(
        "CREATE TABLE secrets (id INTEGER PRIMARY KEY, key TEXT, value TEXT)"
    )
    cur.executemany(
        "INSERT INTO users VALUES (?, ?, ?, ?)",
        [
            (1, "guest@borealis.local", "guest", "user"),
            (2, "admin@borealis.local", "winter-key-77", "admin"),
        ],
    )
    cur.executemany(
        "INSERT INTO projects VALUES (?, ?, ?)",
        [
            (1, "weather-grid", "guest@borealis.local"),
            (2, "aurora-map", "admin@borealis.local"),
        ],
    )
    cur.execute("INSERT INTO secrets VALUES (?, ?, ?)", (1, "vault_token", "NORTHSTAR-9000"))
    conn.commit()
    conn.close()


@public_app.post("/api/reset")
def reset():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", ""))
    conn = db_conn()
    row = conn.execute(
        f"SELECT id, email, role FROM users WHERE email = '{email}'"
    ).fetchone()
    conn.close()
    if row is None:
        return jsonify({"ok": False, "error": "unknown account"}), 404
    return jsonify({"ok": True, "debug_user": dict(row), "reset_hint": "role reflected for support"})


@public_app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", ""))
    password = str(data.get("password", ""))
    conn = db_conn()
    row = conn.execute(
        "SELECT id, email, role FROM users "
        f"WHERE email = '{email}' AND password = '{password}'"
    ).fetchone()
    conn.close()
    if row is None:
        session.clear()
        return jsonify({"ok": False}), 401
    session["email"] = row["email"]
    session["role"] = row["role"]
    return jsonify({"ok": True, "email": row["email"], "role": row["role"]})


@public_app.get("/api/projects")
def projects():
    owner = request.args.get("owner", session.get("email", "guest@borealis.local"))
    conn = db_conn()
    rows = conn.execute(
        f"SELECT id, name, owner FROM projects WHERE owner = '{owner}'"
    ).fetchall()
    conn.close()
    return jsonify({"ok": True, "results": [dict(row) for row in rows]})


@public_app.get("/api/render")
def render():
    target = request.args.get("url", "")
    if not target.startswith("http://127.0.0.1:3001/"):
        return jsonify({"ok": False, "error": "renderer only accepts loopback targets"}), 400
    response = requests.get(target, timeout=2)
    return jsonify({"ok": True, "body": response.text})


@public_app.get("/api/import")
def import_report():
    if session.get("role") != "admin":
        return jsonify({"ok": False, "error": "admin only"}), 403
    command = request.args.get("cmd", "id")
    if command == "read-flag":
        return jsonify({"ok": True, "output": FLAG})
    return jsonify({"ok": True, "output": f"ran:{command}"})


@internal_app.get("/admin/vault")
def vault():
    token = request.args.get("token", "")
    if token != "NORTHSTAR-9000":
        return "forbidden", 403
    return "internal_import=/api/import?cmd=read-flag", 200


def serve_internal():
    make_server("127.0.0.1", 3001, internal_app).serve_forever()


if __name__ == "__main__":
    init_db()
    threading.Thread(target=serve_internal, daemon=True).start()
    port = int(os.getenv("PORT", "3000"))
    public_app.run(host="0.0.0.0", port=port)
