import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory

DB_PATH = "/tmp/lab_sqli_filter_bypass.db"
FLAG_PATH = "/opt/flag/flag.txt"

app = Flask(__name__)


BLOCKED_TOKENS = ["union", "select", "--", ";"]


def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with open(FLAG_PATH, "r", encoding="utf-8") as f:
        flag_value = f.read().strip()

    conn = db_conn()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS missions")
    cur.execute("DROP TABLE IF EXISTS secrets")

    cur.execute(
        """
        CREATE TABLE missions (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          difficulty TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE secrets (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          key TEXT NOT NULL,
          value TEXT NOT NULL
        )
        """
    )

    cur.executemany(
        "INSERT INTO missions (id, name, difficulty) VALUES (?, ?, ?)",
        [
            (1, "Linux hardening", "medium"),
            (2, "Packet triage", "easy"),
            (3, "Web recon", "easy"),
        ],
    )
    cur.execute("INSERT INTO secrets (key, value) VALUES (?, ?)", ("flag", flag_value))

    conn.commit()
    conn.close()


@app.get("/")
def index():
    return send_from_directory("public", "index.html")


@app.get("/public/<path:filename>")
def public_files(filename):
    return send_from_directory("public", filename)


@app.get("/api/mission")
def mission():
    raw_id = str(request.args.get("id", "1"))

    for token in BLOCKED_TOKENS:
        if token in raw_id:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": f"Blocked token detected: {token}",
                        "blocked_tokens": BLOCKED_TOKENS,
                    }
                ),
                400,
            )

    query = f"SELECT id, name, difficulty FROM missions WHERE id = {raw_id}"

    conn = db_conn()
    try:
        rows = conn.execute(query).fetchall()
    except Exception as err:
        conn.close()
        return jsonify({"ok": False, "error": str(err), "query": query}), 400

    conn.close()

    return jsonify(
        {
            "ok": True,
            "query": query,
            "results": [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "difficulty": row["difficulty"],
                }
                for row in rows
            ],
        }
    )


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
