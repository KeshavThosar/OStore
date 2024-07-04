from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import setup_db

app = Flask(__name__)
db = setup_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)



