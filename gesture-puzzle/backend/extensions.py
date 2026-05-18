# backend/extensions.py
# Shared extension instances — imported by app.py AND routes.
# This pattern avoids circular imports in Flask.
#
# Why a separate file?
#   app.py creates the Flask app.
#   routes/scores.py needs db and socketio.
#   If routes imported from app.py, you'd get a circular import.
#   Solution: both import from this neutral extensions.py file.

from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db       = SQLAlchemy()
socketio = SocketIO()
