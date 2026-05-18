# backend/socket_events.py
# Flask-SocketIO event handlers.
# Import this file in app.py AFTER socketio is initialised
# so the @socketio.on decorators register correctly.
#
# Socket.IO replaces the WebSocket endpoint from the FastAPI version.
# The pattern is simpler: the client connects, and we push events to it.
# Broadcasting is done from routes/scores.py via socketio.emit().

from extensions import socketio


@socketio.on("connect")
def on_connect():
    """Fires when a browser tab connects to the Socket.IO server."""
    print(f"[SocketIO] Client connected")
    # You could emit the current leaderboard immediately on connect:
    # from models import Score
    # from routes.scores import _get_leaderboard
    # emit("leaderboard_update", {"data": _get_leaderboard()})


@socketio.on("disconnect")
def on_disconnect():
    print(f"[SocketIO] Client disconnected")


@socketio.on("ping_server")
def on_ping(data):
    """Optional: client can send a ping to check connection health."""
    socketio.emit("pong_client", {"status": "alive"})
