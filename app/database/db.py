from flask import Flask
from .models import get_db

def setup_db(app: Flask):
    '''
    Adds the database connection to the Flask app 
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ostore.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = get_db()
    db.init_app(app)
    return db
