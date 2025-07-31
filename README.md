# TourGuide Connect

A comprehensive platform connecting tourists with knowledgeable local guides for personalized travel experiences. Built with Flask, SQLAlchemy, and Bootstrap.

## 🌟 Features

### For Tourists
- **Browse Tours**: Discover amazing experiences with local guides
- **Advanced Search**: Filter tours by location, category, price, and duration
- **Booking System**: Easy tour booking with date selection and special requests
- **Review System**: Rate and review completed tours
- **User Profiles**: Manage personal information and preferences
- **Booking History**: Track all your tour bookings

### For Guides
- **Tour Creation**: Create and manage detailed tour listings
- **Profile Management**: Showcase expertise, languages, and experience
- **Booking Management**: Handle tour bookings and confirmations
- **Earnings Tracking**: Monitor tour earnings and statistics
- **Review Management**: View and respond to tourist reviews

### Platform Features
- **User Authentication**: Secure registration and login system
- **Responsive Design**: Mobile-friendly interface
- **Real-time Search**: Instant tour search and filtering
- **Rating System**: 5-star rating system with detailed reviews
- **Modern UI**: Beautiful, intuitive interface with Bootstrap 5

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GuideFinder
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python app.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
GuideFinder/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── forms.py              # WTForms for form handling
├── requirements.txt      # Python dependencies
├── create_db.py         # Database initialization script
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── profile.html     # User profile page
│   ├── tours.html       # Tours listing page
│   ├── tour_detail.html # Individual tour page
│   ├── book_tour.html   # Tour booking page
│   ├── dashboard.html   # User dashboard
│   ├── create_tour.html # Tour creation page
│   ├── my_bookings.html # Bookings management
│   ├── guide_profile.html # Guide profile page
│   ├── review_booking.html # Review form
│   └── search_results.html # Search results page
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Custom CSS styles
│   ├── js/
│   │   └── script.js    # Custom JavaScript
│   └── images/          # Image assets
└── README.md           # Project documentation
```

## 🗄️ Database Models

### User
- Basic user information (username, email, password)
- User type (tourist/guide)
- Profile information (bio, location, languages, experience)
- Guide-specific fields (skills, hourly rate, verification status)
- Rating and review statistics

### Tour
- Tour details (title, description, category, location)
- Pricing and capacity (price, max group size)
- Tour logistics (duration, meeting point, requirements)
- Guide association and status

### Booking
- Booking information (date, number of people, total price)
- Status tracking (pending, confirmed, completed, cancelled)
- Tourist and tour associations
- Special requests and notes

### Review
- Rating system (1-5 stars)
- Detailed comments and feedback
- Associations with booking, tour, guide, and tourist
- Timestamp and moderation support

## 🎨 UI/UX Features

### Design System
- **Bootstrap 5**: Modern, responsive framework
- **Font Awesome**: Professional icons
- **Custom CSS**: Enhanced styling and animations
- **Mobile-First**: Responsive design for all devices

### Interactive Elements
- **Hover Effects**: Smooth transitions and animations
- **Form Validation**: Real-time validation with helpful feedback
- **Rating System**: Interactive star rating interface
- **Search Filters**: Dynamic filtering and sorting
- **Loading States**: User feedback during operations

### User Experience
- **Intuitive Navigation**: Clear menu structure and breadcrumbs
- **Progressive Disclosure**: Information revealed as needed
- **Consistent Design**: Unified visual language throughout
- **Accessibility**: Keyboard navigation and screen reader support

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///site.db
FLASK_ENV=development
```

### Database Configuration
The application uses SQLite by default. For production, consider using PostgreSQL or MySQL:

```python
# For PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/tourguide'

# For MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/tourguide'
```

## 🚀 Deployment

### Local Development
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Production Deployment
1. **Set up a production server** (e.g., Ubuntu with Nginx)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
   ```
3. **Configure environment variables**
4. **Set up database** (PostgreSQL recommended for production)
5. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## 🔒 Security Features

- **Password Hashing**: Secure password storage with Werkzeug
- **CSRF Protection**: Built-in CSRF token protection
- **Form Validation**: Server-side and client-side validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **XSS Protection**: Template escaping and sanitization

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- **Mobile phones** (320px+)
- **Tablets** (768px+)
- **Desktop** (1024px+)
- **Large screens** (1200px+)

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Tour creation and editing
- [ ] Tour booking process
- [ ] Search and filtering
- [ ] Review submission
- [ ] Profile management
- [ ] Mobile responsiveness
- [ ] Form validation

### Automated Testing (Future Enhancement)
```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/
```

## 🔄 Future Enhancements

### Planned Features
- **Real-time Chat**: Direct messaging between tourists and guides
- **Payment Integration**: Secure payment processing
- **Image Upload**: Profile and tour image management
- **Email Notifications**: Booking confirmations and updates
- **Advanced Analytics**: Detailed insights for guides
- **Multi-language Support**: Internationalization
- **API Development**: RESTful API for mobile apps
- **Push Notifications**: Real-time updates

### Technical Improvements
- **Caching**: Redis integration for performance
- **Background Jobs**: Celery for async tasks
- **Monitoring**: Application performance monitoring
- **CI/CD**: Automated testing and deployment
- **Docker**: Containerization for easy deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation

## 🙏 Acknowledgments

- **Flask**: Web framework
- **Bootstrap**: CSS framework
- **Font Awesome**: Icons
- **SQLAlchemy**: Database ORM
- **WTForms**: Form handling

---

**TourGuide Connect** - Connecting travelers with amazing local experiences! 🌍✨
