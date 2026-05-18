# backend/models.py
from datetime import datetime
from extensions import db


class Score(db.Model):
    __tablename__ = "scores"

    id           = db.Column(db.Integer, primary_key=True)
    player_name  = db.Column(db.String(64),  nullable=False)
    time_seconds = db.Column(db.Float,       nullable=False)   # solve time in seconds
    move_count   = db.Column(db.Integer,     nullable=False)   # number of tile swaps
    puzzle_image = db.Column(db.Text,        nullable=True)    # optional base64 JPEG
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self, rank: int = None) -> dict:
        """Serialize to a plain dict for JSON responses."""
        d = {
            "id":           self.id,
            "player_name":  self.player_name,
            "time_seconds": self.time_seconds,
            "move_count":   self.move_count,
            "created_at":   self.created_at.isoformat(),
        }
        if rank is not None:
            d["rank"] = rank
        return d

    def __repr__(self):
        return f"<Score id={self.id} player={self.player_name} time={self.time_seconds:.1f}s>"
