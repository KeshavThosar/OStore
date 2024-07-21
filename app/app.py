'''
The main file that runs the server for flask 
'''
import os

from flask import Flask, render_template
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

storage = Storage(auth, db)
app.add_url_rule('/storage/<endpoint>', 'storage', storage.handle_endpoint, methods=['GET', 'POST', 'PUT', 'DELETE'])

@app.route('/')
def home():
  test_access_token = os.environ['long_exp_access_tok'] #For testing
  test_access_token = ''
  return render_template('index.html', test_token=test_access_token)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY'] 
app.config['JWT_TOKEN_LOCATION'] = ['headers']

if __name__ == '__main__':
  app.run(port=os.environ['PORT'], debug=True)
  
