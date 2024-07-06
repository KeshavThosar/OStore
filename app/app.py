'''
The main file that runs the server for flask 
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import setup_db
from api.storage import Storage

app = Flask(__name__)
db = setup_db(app)

with app.app_context():
  db.create_all()
  
storage = Storage(db)
app.add_url_rule('/storage/<endpoint>', 'storage', storage.handle_endpoint, methods=['GET', 'POST', 'PUT', 'DELETE'])

if __name__ == '__main__':
  app.run(port=5000, debug=True)



