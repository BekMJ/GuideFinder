from app import db
from flask_login import UserMixin
from datetime import datetime

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
    skills = db.Column(db.String(200), nullable=True)
    interests = db.Column(db.String(200), nullable=True)
    hourly_rate = db.Column(db.Float, nullable=True)
    profile_image = db.Column(db.String(200), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    
    # Relationships
    tours = db.relationship('Tour', backref='guide', lazy=True)
    bookings_as_tourist = db.relationship('Booking', foreign_keys='Booking.tourist_id', backref='tourist', lazy=True)
    reviews_received = db.relationship('Review', foreign_keys='Review.guide_id', backref='guide', lazy=True)
    reviews_given = db.relationship('Review', foreign_keys='Review.tourist_id', backref='tourist', lazy=True)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in hours
    price = db.Column(db.Float, nullable=False)
    max_group_size = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # historical, adventure, food, etc.
    location = db.Column(db.String(100), nullable=False)
    meeting_point = db.Column(db.String(200), nullable=False)
    included_items = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bookings = db.relationship('Booking', backref='tour', lazy=True)
    reviews = db.relationship('Review', backref='tour', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    special_requests = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tourist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tourist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
