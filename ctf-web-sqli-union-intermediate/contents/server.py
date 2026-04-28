import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory

DB_PATH = "/tmp/lab_sqli_union.db"
FLAG_PATH = "/opt/flag/flag.txt"

app = Flask(__name__)


def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with open(FLAG_PATH, "r", encoding="utf-8") as f:
        flag_value = f.read().strip()

    conn = db_conn()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("DROP TABLE IF EXISTS secrets")

    cur.execute(
        """
        CREATE TABLE products (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          price REAL NOT NULL
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
        "INSERT INTO products (name, price) VALUES (?, ?)",
        [
            ("Orbit Mouse", 39.0),
            ("Solar Keyboard", 89.0),
            ("Titanium Laptop Stand", 59.0),
            ("Telemetry Webcam", 109.0),
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


@app.get("/api/search")
def search():
    q = str(request.args.get("q", ""))
    query = (
        "SELECT id, name, price FROM products "
        f"WHERE name LIKE '%{q}%'"
    )

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
                    "price": row["price"],
                }
                for row in rows
            ],
        }
    )


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
