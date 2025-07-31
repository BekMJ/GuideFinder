from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, FloatField, DateField, TimeField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional
from datetime import datetime, timedelta

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('tourist', 'Tourist'), ('guide', 'Guide')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    languages = StringField('Languages (comma-separated)', validators=[Optional()])
    experience = StringField('Experience', validators=[Optional()])
    skills = StringField('Skills (comma-separated)', validators=[Optional()])
    interests = StringField('Interests (comma-separated)', validators=[Optional()])
    hourly_rate = FloatField('Hourly Rate ($)', validators=[Optional(), NumberRange(min=0)])
    profile_image = FileField('Profile Image')
    submit = SubmitField('Update Profile')

class TourForm(FlaskForm):
    title = StringField('Tour Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    duration = IntegerField('Duration (hours)', validators=[DataRequired(), NumberRange(min=1, max=24)])
    price = FloatField('Price per person ($)', validators=[DataRequired(), NumberRange(min=0)])
    max_group_size = IntegerField('Maximum Group Size', validators=[DataRequired(), NumberRange(min=1, max=50)])
    category = SelectField('Category', choices=[
        ('historical', 'Historical'),
        ('adventure', 'Adventure'),
        ('food', 'Food & Culinary'),
        ('cultural', 'Cultural'),
        ('nature', 'Nature & Wildlife'),
        ('city', 'City Highlights'),
        ('art', 'Art & Museums'),
        ('photography', 'Photography'),
        ('shopping', 'Shopping'),
        ('nightlife', 'Nightlife'),
        ('other', 'Other')
    ])
    location = StringField('Location', validators=[DataRequired()])
    meeting_point = StringField('Meeting Point', validators=[DataRequired()])
    included_items = TextAreaField('What\'s Included', validators=[Optional()])
    requirements = TextAreaField('Requirements', validators=[Optional()])
    image_url = StringField('Image URL', validators=[Optional()])
    submit = SubmitField('Create Tour')

class BookingForm(FlaskForm):
    booking_date = DateField('Tour Date', validators=[DataRequired()])
    number_of_people = IntegerField('Number of People', validators=[DataRequired(), NumberRange(min=1, max=20)])
    special_requests = TextAreaField('Special Requests', validators=[Optional()])
    submit = SubmitField('Book Tour')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, '⭐⭐⭐⭐⭐ Excellent'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (3, '⭐⭐⭐ Good'),
        (2, '⭐⭐ Fair'),
        (1, '⭐ Poor')
    ], coerce=int, validators=[DataRequired()])
    comment = TextAreaField('Review', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Review')

class SearchForm(FlaskForm):
    location = StringField('Location', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('historical', 'Historical'),
        ('adventure', 'Adventure'),
        ('food', 'Food & Culinary'),
        ('cultural', 'Cultural'),
        ('nature', 'Nature & Wildlife'),
        ('city', 'City Highlights'),
        ('art', 'Art & Museums'),
        ('photography', 'Photography'),
        ('shopping', 'Shopping'),
        ('nightlife', 'Nightlife'),
        ('other', 'Other')
    ])
    max_price = FloatField('Max Price ($)', validators=[Optional(), NumberRange(min=0)])
    duration = SelectField('Duration', choices=[
        ('', 'Any Duration'),
        ('1-2', '1-2 hours'),
        ('3-4', '3-4 hours'),
        ('5-6', '5-6 hours'),
        ('7+', '7+ hours')
    ])
    submit = SubmitField('Search Tours')