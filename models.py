from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, default=0.0)
