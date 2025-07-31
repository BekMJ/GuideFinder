from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm, ProfileForm, TourForm, BookingForm, ReviewForm, SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import models after db initialization
from models import User, Tour, Booking, Review

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/index")
def index():
    # Get featured tours
    featured_tours = Tour.query.filter_by(is_active=True).order_by(Tour.created_at.desc()).limit(6).all()
    # Get top-rated guides
    top_guides = User.query.filter_by(user_type='guide').order_by(User.rating.desc()).limit(4).all()
    return render_template('index.html', featured_tours=featured_tours, top_guides=top_guides)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            hashed_password = generate_password_hash(form.password.data)
            user = User(
                username=form.username.data, 
                email=form.email.data, 
                password=hashed_password, 
                user_type=form.user_type.data
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('An account with this email already exists.', 'danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.languages = form.languages.data
        current_user.experience = form.experience.data
        current_user.skills = form.skills.data
        current_user.interests = form.interests.data
        current_user.hourly_rate = form.hourly_rate.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.languages.data = current_user.languages
        form.experience.data = current_user.experience
        form.skills.data = current_user.skills
        form.interests.data = current_user.interests
        form.hourly_rate.data = current_user.hourly_rate
    
    return render_template('profile.html', form=form, user=current_user)

@app.route("/tours")
def tours():
    page = request.args.get('page', 1, type=int)
    tours = Tour.query.filter_by(is_active=True).order_by(Tour.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('tours.html', tours=tours)

@app.route("/tour/<int:tour_id>")
def tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    reviews = Review.query.filter_by(tour_id=tour_id).order_by(Review.created_at.desc()).all()
    return render_template('tour_detail.html', tour=tour, reviews=reviews)

@app.route("/tour/create", methods=['GET', 'POST'])
@login_required
def create_tour():
    if current_user.user_type != 'guide':
        flash('Only guides can create tours.', 'danger')
        return redirect(url_for('index'))
    
    form = TourForm()
    if form.validate_on_submit():
        tour = Tour(
            title=form.title.data,
            description=form.description.data,
            duration=form.duration.data,
            price=form.price.data,
            max_group_size=form.max_group_size.data,
            category=form.category.data,
            location=form.location.data,
            meeting_point=form.meeting_point.data,
            included_items=form.included_items.data,
            requirements=form.requirements.data,
            image_url=form.image_url.data,
            guide_id=current_user.id
        )
        db.session.add(tour)
        db.session.commit()
        flash('Tour created successfully!', 'success')
        return redirect(url_for('tour_detail', tour_id=tour.id))
    
    return render_template('create_tour.html', form=form)

@app.route("/tour/<int:tour_id>/book", methods=['GET', 'POST'])
@login_required
def book_tour(tour_id):
    if current_user.user_type != 'tourist':
        flash('Only tourists can book tours.', 'danger')
        return redirect(url_for('tour_detail', tour_id=tour_id))
    
    tour = Tour.query.get_or_404(tour_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        total_price = tour.price * form.number_of_people.data
        booking = Booking(
            booking_date=form.booking_date.data,
            number_of_people=form.number_of_people.data,
            total_price=total_price,
            special_requests=form.special_requests.data,
            tourist_id=current_user.id,
            tour_id=tour_id
        )
        db.session.add(booking)
        db.session.commit()
        flash('Tour booked successfully!', 'success')
        return redirect(url_for('my_bookings'))
    
    return render_template('book_tour.html', form=form, tour=tour)

@app.route("/my-bookings")
@login_required
def my_bookings():
    if current_user.user_type == 'tourist':
        bookings = Booking.query.filter_by(tourist_id=current_user.id).order_by(Booking.created_at.desc()).all()
    else:
        bookings = Booking.query.join(Tour).filter(Tour.guide_id == current_user.id).order_by(Booking.created_at.desc()).all()
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route("/booking/<int:booking_id>/review", methods=['GET', 'POST'])
@login_required
def review_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.tourist_id != current_user.id:
        flash('You can only review your own bookings.', 'danger')
        return redirect(url_for('my_bookings'))
    
    if booking.status != 'completed':
        flash('You can only review completed bookings.', 'danger')
        return redirect(url_for('my_bookings'))
    
    # Check if review already exists
    existing_review = Review.query.filter_by(booking_id=booking_id).first()
    if existing_review:
        flash('You have already reviewed this booking.', 'danger')
        return redirect(url_for('my_bookings'))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            comment=form.comment.data,
            tourist_id=current_user.id,
            guide_id=booking.tour.guide_id,
            tour_id=booking.tour_id,
            booking_id=booking_id
        )
        db.session.add(review)
        
        # Update guide's rating
        guide = booking.tour.guide
        guide.total_reviews += 1
        all_reviews = Review.query.filter_by(guide_id=guide.id).all()
        guide.rating = sum(r.rating for r in all_reviews) / len(all_reviews)
        
        db.session.commit()
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('my_bookings'))
    
    return render_template('review_booking.html', form=form, booking=booking)

@app.route("/guide/<int:guide_id>")
def guide_profile(guide_id):
    guide = User.query.get_or_404(guide_id)
    if guide.user_type != 'guide':
        flash('User is not a guide.', 'danger')
        return redirect(url_for('index'))
    
    tours = Tour.query.filter_by(guide_id=guide_id, is_active=True).all()
    reviews = Review.query.filter_by(guide_id=guide_id).order_by(Review.created_at.desc()).all()
    
    return render_template('guide_profile.html', guide=guide, tours=tours, reviews=reviews)

@app.route("/search")
def search_tours():
    form = SearchForm()
    tours = Tour.query.filter_by(is_active=True)
    
    if form.location.data:
        tours = tours.filter(Tour.location.ilike(f'%{form.location.data}%'))
    if form.category.data:
        tours = tours.filter(Tour.category == form.category.data)
    if form.max_price.data:
        tours = tours.filter(Tour.price <= form.max_price.data)
    if form.duration.data:
        if form.duration.data == '1-2':
            tours = tours.filter(Tour.duration.between(1, 2))
        elif form.duration.data == '3-4':
            tours = tours.filter(Tour.duration.between(3, 4))
        elif form.duration.data == '5-6':
            tours = tours.filter(Tour.duration.between(5, 6))
        elif form.duration.data == '7+':
            tours = tours.filter(Tour.duration >= 7)
    
    tours = tours.order_by(Tour.created_at.desc()).all()
    return render_template('search_results.html', tours=tours, form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.user_type == 'guide':
        tours = Tour.query.filter_by(guide_id=current_user.id).all()
        bookings = Booking.query.join(Tour).filter(Tour.guide_id == current_user.id).all()
        total_earnings = sum(booking.total_price for booking in bookings if booking.status == 'completed')
    else:
        tours = []
        bookings = Booking.query.filter_by(tourist_id=current_user.id).all()
        total_earnings = 0
    
    return render_template('dashboard.html', tours=tours, bookings=bookings, total_earnings=total_earnings)

@app.route("/api/tours")
def api_tours():
    tours = Tour.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': tour.id,
        'title': tour.title,
        'description': tour.description,
        'price': tour.price,
        'duration': tour.duration,
        'location': tour.location,
        'category': tour.category,
        'guide_name': tour.guide.username
    } for tour in tours])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)