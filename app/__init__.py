import os
import sqlite3
import tempfile

from dotenv import load_dotenv
from flask import Flask, redirect, render_template
from flask_cors import CORS
from flask_restx import Api

load_dotenv()

_test_db_path = None


def get_db_path():
    if _test_db_path:
        return _test_db_path
    return os.getenv("DATABASE_PATH", "data/app.db")


def get_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    db_path = get_db_path()
    if db_path != ":memory:":
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def create_app(testing=False):
    global _test_db_path
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["TESTING"] = testing

    if testing:
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        _test_db_path = tmp.name

    CORS(app)

    authorizations = {
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY",
        }
    }

    api = Api(
        app,
        version="1.0",
        title="User Registration API",
        description="Demo RESTful API untuk materi kuliah — CRUD, Auth, Docker, CI/CD",
        doc="/docs",
        authorizations=authorizations,
        security="apikey",
    )

    from app.routes import ns

    api.add_namespace(ns, path="/api")

    @app.route("/")
    def index():
        return redirect("/app")

    @app.route("/app")
    def user_app():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return {"status": "healthy"}

    init_db()

    return app
