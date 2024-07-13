'''
Model classes for database
'''

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def get_db():
  return db


# Model Declarations
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  # first_name = db.Column(db.String(50), nullable=False)
  # last_name = db.Column(db.String(50), nullable=False)
  password_hash = db.Column(db.String(256), nullable=False)
  store_objects = db.relationship('StoreObject', backref='user', lazy=True)


class StoreObject(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  file_name = db.Column(db.String(256), unique=True, nullable=False)
  file_hash = db.Column(db.String(256), nullable=False)
  file_identifier = db.Column(db.String(36), nullable=False)
  creation_datetime = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


