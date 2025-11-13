# config.py
import os

class Config:
    # PythonAnywhere MySQL database configuration
    # These will be set later when you create the database
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL connection string format for PythonAnywhere
    # Format: mysql+pymysql://username:password@username.mysql.pythonanywhere-services.com/username$dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://yourusername:password@yourusername.mysql.pythonanywhere-services.com/yourusername$peardb'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False