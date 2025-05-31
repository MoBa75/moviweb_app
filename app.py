from flask import Flask
from data_models import db, User, Movie, UserMovies
from db_validation import validate_database
import os
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'movies.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)

validate_database(app)

@app.route()
def add_user():
    pass

@app.route()
def choose_user():
    pass

@app.route()
def delete_user():
    pass

@app.route()
def show_movies():
    pass

@app.route()
def add_movie():
    pass

@app.route()
def update_movie():
    pass

@app.route()
def delete_movie():
    pass

app.route()
def user_rating():
    pass