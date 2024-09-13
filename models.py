from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'tourist' or 'guide'
    # Guide-specific fields
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    languages = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.String(200), nullable=True)
