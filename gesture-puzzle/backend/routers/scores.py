# backend/routes/scores.py
# Blueprint for all score-related routes.
# Registered in app.py with url_prefix="/api".

from flask import Blueprint, request, jsonify, abort
from extensions import db, socketio
from models import Score

scores_bp = Blueprint("scores", __name__)

LEADERBOARD_SIZE = 10


# ── POST /api/scores ──────────────────────────────────────────────────────────
@scores_bp.post("/scores")
def submit_score():
    """
    Called by the frontend when a puzzle is solved.
    Saves the score, then broadcasts the updated leaderboard
    to every connected Socket.IO client.
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="JSON body required")

    # Basic validation
    player_name  = str(data.get("player_name", "")).strip()
    time_seconds = data.get("time_seconds")
    move_count   = data.get("move_count")

    if not player_name:
        abort(400, description="player_name is required")
    if not isinstance(time_seconds, (int, float)) or time_seconds <= 0:
        abort(400, description="time_seconds must be a positive number")
    if not isinstance(move_count, int) or move_count < 0:
        abort(400, description="move_count must be a non-negative integer")

    score = Score(
        player_name  = player_name[:64],
        time_seconds = float(time_seconds),
        move_count   = int(move_count),
        puzzle_image = data.get("puzzle_image"),   # optional base64 string
    )
    db.session.add(score)
    db.session.commit()

    # Broadcast updated leaderboard to all Socket.IO clients
    leaderboard = _get_leaderboard()
    socketio.emit("leaderboard_update", {"data": leaderboard})

    return jsonify(score.to_dict()), 201


# ── GET /api/scores ───────────────────────────────────────────────────────────
@scores_bp.get("/scores")
def get_leaderboard():
    """Return top-N scores sorted by time ascending (fastest first)."""
    return jsonify(_get_leaderboard())


# ── GET /api/scores/<id> ──────────────────────────────────────────────────────
@scores_bp.get("/scores/<int:score_id>")
def get_score(score_id: int):
    score = db.session.get(Score, score_id)
    if not score:
        abort(404, description="Score not found")
    return jsonify(score.to_dict())


# ── DELETE /api/scores/<id> ───────────────────────────────────────────────────
@scores_bp.delete("/scores/<int:score_id>")
def delete_score(score_id: int):
    score = db.session.get(Score, score_id)
    if not score:
        abort(404, description="Score not found")
    db.session.delete(score)
    db.session.commit()
    return "", 204


# ── POST /api/process-image ───────────────────────────────────────────────────
# Optional server-side OpenCV processing.
# Send a base64 JPEG from the frontend, get a processed one back.
@scores_bp.post("/process-image")
def process_image():
    """
    Receives a base64 JPEG, applies an OpenCV effect, returns processed base64.

    Body:  { "image_base64": "...", "effect": "blur" | "edge" | "gray" | "none" }
    """
    try:
        import cv2
        import numpy as np
        import base64
    except ImportError:
        abort(503, description="OpenCV is not installed on this server")

    data = request.get_json(silent=True)
    if not data or "image_base64" not in data:
        abort(400, description="image_base64 field is required")

    # base64 → numpy array → OpenCV BGR image
    try:
        img_bytes = base64.b64decode(data["image_base64"])
        np_arr    = np.frombuffer(img_bytes, np.uint8)
        img       = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception:
        abort(400, description="Could not decode image")

    if img is None:
        abort(400, description="Invalid image data")

    # Apply effect
    effect = str(data.get("effect", "none")).lower()
    if effect == "gray":
        processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    elif effect == "blur":
        processed = cv2.GaussianBlur(img, (21, 21), 0)
    elif effect == "edge":
        gray      = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges     = cv2.Canny(gray, 50, 150)
        processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    else:
        processed = img  # no-op

    # OpenCV image → base64 JPEG
    _, buffer   = cv2.imencode(".jpg", processed, [cv2.IMWRITE_JPEG_QUALITY, 90])
    result_b64  = base64.b64encode(buffer).decode("utf-8")

    return jsonify({"image_base64": result_b64})


# ── Error handlers ────────────────────────────────────────────────────────────
@scores_bp.errorhandler(400)
@scores_bp.errorhandler(404)
@scores_bp.errorhandler(503)
def handle_error(e):
    return jsonify({"error": str(e.description)}), e.code


# ── Private helper ────────────────────────────────────────────────────────────
def _get_leaderboard() -> list[dict]:
    scores = (
        Score.query
        .order_by(Score.time_seconds.asc())
        .limit(LEADERBOARD_SIZE)
        .all()
    )
    return [s.to_dict(rank=i + 1) for i, s in enumerate(scores)]
