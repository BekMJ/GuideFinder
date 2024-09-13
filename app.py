from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm, ProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Add this line

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'tourist' or 'guide'
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    languages = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.String(200), nullable=True)
    skills = db.Column(db.String(200), nullable=True)  # Add this line
    interests = db.Column(db.String(200), nullable=True)  # Add this line

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data, user_type=form.user_type.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        else:
            flash('An account with this email already exists.', 'danger')
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
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
    user = current_user  # Make sure current_user is not None
    if request.method == 'POST' and form.validate_on_submit():
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.languages = form.languages.data
        current_user.experience = form.experience.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.languages.data = current_user.languages
        form.experience.data = current_user.experience
    return render_template('profile.html', form=form, user=user)

@app.route("/guide/<int:guide_id>")
def guide_profile(guide_id):
    guide = User.query.get_or_404(guide_id)
    if guide.user_type != 'guide':
        flash('User is not a guide.', 'danger')
        return redirect(url_for('index'))
    return render_template('guide_profile.html', guide=guide)

if __name__ == '__main__':
    app.run(debug=True)