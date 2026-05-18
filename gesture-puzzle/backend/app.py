# backend/app.py
# Flask entry point — run this file to start the server.
#
#   python app.py            ← development (debug mode, auto-reload)
#   flask run --port 8000    ← also works

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

from extensions import db, socketio
from routes.scores import scores_bp

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    # ── Config ────────────────────────────────────────────────────────────────
    app.config["SECRET_KEY"]           = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///puzzle.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── CORS ──────────────────────────────────────────────────────────────────
    # Allow the Vite dev server at :5173 to call this backend.
    CORS(app, origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173"))

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    socketio.init_app(
        app,
        cors_allowed_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173"),
        async_mode="threading",   # simple threading mode — no asyncio needed
    )

    # ── Blueprints (routers) ──────────────────────────────────────────────────
    app.register_blueprint(scores_bp, url_prefix="/api")

    # ── Create DB tables on first run ─────────────────────────────────────────
    with app.app_context():
        db.create_all()

    # ── Health check ─────────────────────────────────────────────────────────
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


# Run directly with `python app.py`
if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
