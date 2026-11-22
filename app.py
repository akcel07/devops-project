import os

import psycopg
from flask import Flask


def create_app():
    app = Flask(__name__)
    database_url = os.environ.get("DATABASE_URL")
    app.config["VISITS"] = 0

    if database_url:
        with psycopg.connect(database_url) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS visits ("
                "id INTEGER PRIMARY KEY, count INTEGER NOT NULL)"
            )
            conn.execute(
                "INSERT INTO visits (id, count) VALUES (1, 0) "
                "ON CONFLICT (id) DO NOTHING"
            )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/visits")
    def visits():
        if database_url:
            with psycopg.connect(database_url) as conn:
                row = conn.execute(
                    "UPDATE visits SET count = count + 1 "
                    "WHERE id = 1 RETURNING count"
                ).fetchone()
            count = row[0]
        else:
            app.config["VISITS"] += 1
            count = app.config["VISITS"]
        return {"visits": count}

    return app