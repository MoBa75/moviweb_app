from pydoc import describe

from flask import Flask, request, render_template, redirect, url_for, abort
from data_models import User, Movie, UserMovies
from db_validation import validate_database
import os
from datamanager.sqlite_data_manager import SQLiteDataManager
from movie_data_api import get_movie_data

app = Flask(__name__)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'movies.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize data manager
data_manager = SQLiteDataManager(app)

# Validate or create database
validate_database(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page route."""
    users, result = data_manager.get_all_users()
    if result != 200:
        abort(result, description=users['error'])

    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user, result = data_manager.get_user_by_name(username)
            if result != 200:
                return render_template('home.html', users=users,
                                       error=user['error'])
            return redirect(url_for('user_movies', user_id=user.id))
    return render_template('home.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """Displays all movies associated with a specific user."""
    movies, result = data_manager.get_user_movies(user_id)
    if result != 200:
        abort(result, description=movies['error'])
    return render_template('user_movies.html', movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Route to add a new user."""
    if request.method == 'POST':
        username = request.form.get('name')
        if not username:
            return render_template('add_user.html', error='Username is required')
        new_user = User(name=username)
        error, result = data_manager.add_user(new_user)
        if result != 200:
            abort(result, description=error['error'])
        return render_template('add_user.html', error='User added successfully')
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Route to update the rating of a movie for a given user."""
    movie, result = data_manager.get_movie(movie_id)
    if result != 200:
        abort(result, description=movie['error'])

    if request.method == 'POST':
        rating = request.form.get('rating')
        if not rating:
            return render_template('edit_movie.html', movie=movie)
        rating_str = rating.replace(',', '.')

        try:
            rating_float = float(rating_str)
            if not 0.0 < rating_float < 10.0:
                return render_template('edit_movie.html', movie=movie,
                                       error="Rating must be between 0 and 10")
        except (ValueError, TypeError):
            return render_template('edit_movie.html', movie=movie,
                                   error="Please enter a valid rating between 0 and 10.")

        error, result = data_manager.update_movie(movie, rating_float)
        if result == 200:
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('edit_movie.html', movie=movie, error=error)

    return render_template('edit_movie.html', movie=movie)


@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    """Adds a new movie to a user's collection."""
    title = request.form.get('title')
    director = request.form.get('director')
    year = request.form.get('year')
    rating = request.form.get('rating')
    poster = request.form.get('poster')

    if all([title, director, year]):
        try:
            year = int(year)

            if rating is None or rating.strip().lower() == "n/a":
                rating = None
            else:
                rating = float(rating.replace(",", "."))
        except (ValueError, TypeError):
            abort(400, description="Invalid rating or year format.")

        new_movie = Movie(title=title, director=director, year=year, rating=rating, poster=poster)
        error, result = data_manager.add_movie(new_movie, user_id)
        if result == 200:
            return redirect(url_for('user_movies', user_id=user_id))
        abort(result, description=error['error'])
    return render_template('error.html', error="Missing movie data")


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Deletes a movie from a user's collection."""
    status, result = data_manager.delete_movie(user_id, movie_id)
    if result != 200:
        abort(result, description=status['error'])
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    """Deletes a user from the system."""
    result, status = data_manager.delete_user(user_id)
    if not status == 200:
        abort(status, description=result['error'])
    return redirect(url_for('home'))


@app.route('/fetch_movie', methods=['GET', 'POST'])
def fetch_movie():
    """Fetches movie data from an external API (OMDb)."""
    user_id = request.args.get('user_id', type=int)  # für GET

    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int) or user_id
        movie_title = request.form.get('title')
        if movie_title:
            movie_data = get_movie_data(movie_title)
            if 'error' in movie_data:
                return render_template('fetch_movie.html',
                                       error=movie_data['error'], user_id=user_id)
            return render_template('fetch_movie.html',
                                   movie=movie_data, user_id=user_id)

    return render_template('fetch_movie.html', user_id=user_id)


@app.errorhandler(400)
def bad_request(error):
    """Handles 400 Bad Request errors."""
    return render_template('error.html', error=error)


@app.errorhandler(404)
def not_found(error):
    """Handles 404 Not Found errors."""
    return render_template('error.html', error=error)


@app.errorhandler(409)
def conflict(error):
    """Handles 409 Conflict errors."""
    return render_template('error.html', error=error)


@app.errorhandler(500)
def internal_error(error):
    """Handles 500 Internal Server errors."""
    return render_template('error.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
