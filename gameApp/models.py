from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Experiments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    experiment_type = db.Column(db.String(20), nullable=False)
    date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

    def serialize(self):
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "email": self.email, "experiment_type": self.experiment_type, "date_completed": self.date_completed.isoformat()}

    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name} ID: {self.id}"