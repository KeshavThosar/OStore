'''
API definitions for the auth api
Currently supported endpoints:
/auth/register - register to the service using an email
/auth/login - retrieve access token using email and password
'''
from hashlib import sha256
from datetime import timedelta

from database.models import User
from .handler import EndpointHandler
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, decode_token


class Auth(EndpointHandler):
  def __init__(self, jwt: JWTManager, db: SQLAlchemy):
    super().__init__({
      'register': self.register,
      'login': self.login
    })
    self.jwt = jwt
    self.db = db
    
  def get_hash(self, data: str):
    return sha256(data.encode()).hexdigest()
  
  def get_user(self, email):
    db_session = self.db.session
    user_fetch = db_session.execute(
      self.db.select(User).filter_by(email=email)
    ).scalar_one_or_none()

    return user_fetch

  def register(self):
    email = request.form['email']
    password = request.form['password']
    password_hash = self.get_hash(password)
    # Add validation

    user = self.get_user(email)
    if user is not None:
      return jsonify({'message': 'Email is already registered'}), 409

    user = User(
      email = email,
      password_hash = password_hash
    )

    db_session = self.db.session
    db_session.add(user)
    db_session.commit()

    return jsonify({'message': 'User created successfully'}), 201


  def login(self):
    email = request.form['email']
    password = request.form['password']
    password_hash = self.get_hash(password)

    user = self.get_user(email)
    if user is None or user.password_hash != password_hash:
      return jsonify({'message': 'invalid email or password'})
    
    expiration_time = timedelta(minutes=15) 
    access_token = create_access_token(
      identity=user.id,
      expires_delta=expiration_time
    )

    return jsonify({
      'message': 'Login successful',
      'access_token': access_token,
      'expires_in': expiration_time.seconds,
    }), 200


