# 🚀 Deployment Guide for TourGuide Connect

This guide will help you deploy your TourGuide Connect application to various hosting platforms.

## 📋 Prerequisites

- Python 3.8 or higher
- Git installed
- A GitHub account
- Basic knowledge of command line

## 🌐 Deployment Options

### 1. **Heroku (Recommended for Beginners)**

#### Setup Steps:

1. **Create a Heroku Account**
   - Go to [heroku.com](https://heroku.com) and sign up

2. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **Create Procfile**
   Create a file named `Procfile` (no extension) in your project root:
   ```
   web: gunicorn app:app
   ```

4. **Update requirements.txt**
   Add these lines to your `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```

5. **Deploy to Heroku**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create Heroku app
   heroku create your-app-name
   
   # Add PostgreSQL database
   heroku addons:create heroku-postgresql:mini
   
   # Set environment variables
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set FLASK_ENV=production
   
   # Deploy
   git add .
   git commit -m "Add Heroku deployment files"
   git push heroku main
   
   # Run database migrations
   heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
   
   # Open your app
   heroku open
   ```

### 2. **PythonAnywhere (Free Hosting)**

#### Setup Steps:

1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://pythonanywhere.com) and sign up

2. **Upload Your Code**
   - Go to "Files" tab
   - Upload your project files or clone from GitHub

3. **Set Up Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 tourguide-env
   pip install -r requirements.txt
   ```

4. **Configure WSGI File**
   - Go to "Web" tab
   - Click on your web app
   - Edit the WSGI file:
   ```python
   import sys
   path = '/home/yourusername/your-project-folder'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Set Environment Variables**
   - Add to WSGI file:
   ```python
   import os
   os.environ['SECRET_KEY'] = 'your-secret-key-here'
   os.environ['FLASK_ENV'] = 'production'
   ```

6. **Reload Web App**
   - Click "Reload" button in the Web tab

### 3. **Railway (Modern Alternative)**

#### Setup Steps:

1. **Connect GitHub Repository**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Configure Environment Variables**
   - Go to "Variables" tab
   - Add:
     - `SECRET_KEY`: your-secret-key-here
     - `FLASK_ENV`: production

3. **Deploy**
   - Railway will automatically deploy when you push to GitHub
   - Your app will be available at the provided URL

### 4. **DigitalOcean App Platform**

#### Setup Steps:

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://digitalocean.com)

2. **Create App**
   - Go to "Apps" section
   - Click "Create App"
   - Connect your GitHub repository

3. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn app:app`

4. **Set Environment Variables**
   - Add your environment variables in the app settings

5. **Deploy**
   - Click "Create Resources"
   - Your app will be deployed automatically

## 🔧 Environment Variables

Set these environment variables in your hosting platform:

```env
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
DATABASE_URL=your-database-url
```

## 🗄️ Database Setup

### For Production (PostgreSQL Recommended):

1. **Install PostgreSQL adapter**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update database URL**
   ```python
   # In app.py
   app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
   ```

3. **Run migrations**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## 🔒 Security Considerations

1. **Change Secret Key**
   - Generate a new secret key for production
   - Use: `python -c "import secrets; print(secrets.token_hex(16))"`

2. **Environment Variables**
   - Never commit sensitive data to Git
   - Use environment variables for all secrets

3. **HTTPS**
   - Most hosting platforms provide HTTPS automatically
   - Ensure your app redirects HTTP to HTTPS

## 📊 Monitoring

### Add Logging:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/tourguide.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('TourGuide Connect startup')
```

## 🚀 Performance Optimization

1. **Enable Caching**
   ```python
   from flask_caching import Cache
   
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

2. **Use CDN for Static Files**
   - Consider using CloudFlare or similar CDN

3. **Database Optimization**
   - Add indexes to frequently queried fields
   - Use connection pooling

## 🔄 Continuous Deployment

### GitHub Actions (Optional):

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

## 📱 Domain Setup

1. **Custom Domain**
   - Most platforms allow custom domains
   - Update DNS settings as instructed by your hosting provider

2. **SSL Certificate**
   - Most platforms provide free SSL certificates
   - Ensure HTTPS is enabled

## 🆘 Troubleshooting

### Common Issues:

1. **Import Errors**
   - Check your `requirements.txt` includes all dependencies
   - Ensure virtual environment is activated

2. **Database Connection**
   - Verify database URL is correct
   - Check database credentials

3. **Static Files Not Loading**
   - Ensure static folder is properly configured
   - Check file permissions

4. **500 Errors**
   - Check application logs
   - Verify environment variables are set

### Getting Help:

- Check your hosting platform's documentation
- Review Flask deployment documentation
- Check application logs for error messages

## 📈 Scaling Considerations

1. **Database Scaling**
   - Consider managed database services
   - Implement database connection pooling

2. **Application Scaling**
   - Use load balancers for multiple instances
   - Implement caching strategies

3. **Monitoring**
   - Set up application monitoring
   - Monitor database performance

---

**Happy Deploying! 🎉**

Your TourGuide Connect application is now ready to serve travelers worldwide! 