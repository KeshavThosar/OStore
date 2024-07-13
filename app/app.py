'''
The main file that runs the server for flask 
'''
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from database import setup_db
from api.storage import Storage
from api.auth import Auth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
db = setup_db(app)

with app.app_context():
  db.create_all()

jwt = JWTManager(app)
auth = Auth(jwt, db)
app.add_url_rule('/auth/<endpoint>', 'auth', auth.handle_endpoint, methods=['POST'])

storage = Storage(db) # Add auth as constructor
app.add_url_rule('/storage/<endpoint>', 'storage', storage.handle_endpoint, methods=['GET', 'POST', 'PUT', 'DELETE'])

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY'] 
app.config['JWT_TOKEN_LOCATION'] = ['headers']

if __name__ == '__main__':
  app.run(port=5000, debug=True)
  
